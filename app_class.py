import flet as ft

class App(ft.UserControl):

    def build(self):
        self.new_task = ft.TextField(hint_text="Nome da sua Tarefa", expand=True)
        self.tasks = ft.Column()

        return ft.Column(
            width=600,
            controls=[
                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked),
                    ]
                ),
                self.tasks
            ]
        )

    def add_clicked(self, event):
        self.tasks.controls.append(ft.Checkbox(label=self.new_task.value))
        self.new_task.value = ""
        self.update()


def main(page: ft.Page):
    page.title = "App All"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()
    alls = App()
    alls2 = App()
    page.add(alls, alls2)

ft.app(target=main, view=ft.AppView.WEB_BROWSER)