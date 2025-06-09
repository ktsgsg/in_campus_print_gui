from textual.app import App, ComposeResult
from textual.widgets import Static, Input, Button
from textual.containers import Vertical, Horizontal, ScrollableContainer
from textual.widgets import DirectoryTree
from textual.widgets import RadioButton, RadioSet,Label
import json
import os,sys
import campus_print.in_campus_print
import campus_print.settings 

class PrintInputApp(App):
    CSS_PATH = "css/style.tcss"
    data ={}
    is_page_sort_enabled = False
    webprint = campus_print.in_campus_print.Webprint(campus_print.settings.getpsw())
    def compose(self) -> ComposeResult:
        with Horizontal():
            # ScrollableContainerでラップしてスクロール可能に
            with ScrollableContainer(id="left"):
                yield Static("ファイルを選択してください:", classes="label")
                self.file_input = Input(placeholder="ファイルパス")
                yield self.file_input

                yield Label("用紙サイズ:",id="text_paper_size",classes="label")
                with RadioSet(id="paper_type",classes="format"):
                    yield RadioButton("A4",name="06")
                    yield RadioButton("A3", name="05")
                yield Label("片面／両面 :",id="text_duplex",classes="label")
                with RadioSet(id="duplex_type",classes="format"):
                    yield RadioButton("片面",name="1")
                    yield RadioButton("両面", name="2")
                yield Label("ページレイアウト:",id="text_print_number_up",classes="label")
                with RadioSet(id="number_up",classes="format"):
                    yield RadioButton("1 in 1",name="1")
                    yield RadioButton("2 in 1", name="2")
                    yield RadioButton("4 in 1", name="4")
                yield Label("配置順:",id="text_print_page_sort",classes="label")
                with RadioSet(id="page_sort",classes="format",disabled=True) :
                    yield RadioButton("左上から右向き",name="1")
                    yield RadioButton("左上から下向き", name="2")
                yield Label("とじ方向:",id="text_print_orientation_edge",classes="label")
                with RadioSet(id="orientation_edge",classes="format") :
                    yield RadioButton("長辺とじ",name="1")
                    yield RadioButton("短辺とじ", name="2")
                yield Label("印刷の向き:",id="text_paper_orientation",classes="label")
                with RadioSet(id="print_orientation",classes="format") :
                    yield RadioButton("縦",name="1")
                    yield RadioButton("横", name="2")

                yield Static("枚数を入力してください:", classes="label")
                self.count_input = Input(placeholder="枚数", type="number",value="1")
                yield self.count_input
                self.text_error = Static("", classes="label")
                yield self.text_error
                yield Button("送信", id="submit_btn")


            with Vertical(id="right"):
                self.dir_tree = DirectoryTree("/")
                yield self.dir_tree
                self.output = Static("印刷したいPDFを選択", classes="result",markup=False)
                yield self.output

    async def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        self.file_input.value = str(event.path)

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        self.data[event.radio_set.id] = event.pressed.name
        if event.radio_set.id == "number_up":
            # ページレイアウトが変更されたときにページ配置のラジオボタンを有効化
            if event.pressed.name in ["4"]:
                self.query_one("#page_sort").disabled = False
                self.is_page_sort_enabled = True
            else:
                self.query_one("#page_sort").disabled = True
                self.is_page_sort_enabled = False
                
    def get_layout_ascii(self):
        number_up = self.data.get("number_up")
        orientation_edge = self.data.get("orientation_edge")
        print_orientation = self.data.get("print_orientation")

        # とじ方向の記号
        edge_map = {
            "1": "┃",  # 長辺とじ
            "2": "━",  # 短辺とじ
        }
        edge_str = edge_map.get(orientation_edge, "")

        # 印刷の向き
        orientation_map = {
            "1": "縦",
            "2": "横"
        }
        orientation_str = orientation_map.get(print_orientation, "")

        # レイアウト本体
        if number_up == "1":
            layout = "[ 1 ]"
        elif number_up == "2":
            layout = "[ 1 | 2 ]"
        elif number_up == "4":
            page_sort = self.data.get("page_sort", "1")
            if page_sort == "1":
                layout = "[ 1 | 2 ]\n[ 3 | 4 ]"
            else:
                layout = "[ 1 | 3 ]\n[ 2 | 4 ]"
        else:
            layout = "レイアウト未選択"

        # 印刷の向きととじ方向を付加
        result = f"印刷の向き: {orientation_str}\nとじ方向: {edge_str}\n{layout}"
        return result

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit_btn":
            # 必須のRadioSetのIDリスト
            required_radios = [
                "paper_type",
                "duplex_type",
                "number_up",
                "orientation_edge",
                "print_orientation"
            ]
            if self.is_page_sort_enabled:
                required_radios.append("page_sort")
            # 未選択のRadioSetをチェック
            missing = [rid for rid in required_radios if rid not in self.data or not self.data[rid]]
            if missing:
                self.text_error.update("すべてのラジオボタンを選択してください")
                return
            #file_inputが空でないことを確認
            if not self.file_input.value:
                self.text_error.update("ファイルパスを入力してください")
                return
            if not os.path.isfile(self.file_input.value):
                self.text_error.update("指定されたファイルが存在しません")
                return
            #file_inputがPDFファイルであることを確認
            if not self.file_input.value.lower().endswith('.pdf'):
                self.text_error.update("PDFファイルを選択してください")
                return
            self.data["copies"] = self.count_input.value
            with open("print_data.json", "w") as f:
                json.dump(self.data, f, indent=4)
            # レイアウト図形を右画面に表示
            layout_ascii = self.get_layout_ascii()
            self.output.update(f"プリントレイアウト:\n{layout_ascii}")
            defaultformat=self.webprint.get_defaultformat()
            newformat = {**defaultformat,**self.data}
            self.webprint.set_printformat(newformat)
            # PDFデータを設定して印刷
            self.webprint.set_pdfdata(self.file_input.value)
            self.webprint.filename = os.path.basename(self.file_input.value)
            code = self.webprint.pdfprint()
            self.text_error.update("送信終了: " + str(code))
            self.file_input.value = ""

if __name__ == "__main__":
    campus_print.settings.getpsw() # 認証情報の取得
    app = PrintInputApp()
    app.run()