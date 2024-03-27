import flet as ft

class Task(ft.UserControl):

    def __init__(self, task_name, task_delete, task_status_change):
        super().__init__()
        self.task_name = task_name
        self.task_delete = task_delete
        self.task_status_change = task_status_change
        self.completed = False


    def build(self):
        self.display_task = ft.Checkbox(value=False, label=self.task_name, on_change=self.status_changed)
        self.edit_name = ft.TextField(expand=1)

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Editar",
                            on_click=self.edit_clicked
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE,
                            tooltip="Deletar",
                            on_click=self.delete_clicked
                        )
                    ]
                )
            ]
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Concluir",
                    on_click=self.save_clicked
                )
            ]
        )
        return ft.Column(controls=[self.display_view, self.edit_view])

    def status_changed(self, event):
        self.completed = self.display_task.value
        self.task_status_change(self)

    def delete_clicked(self, event):
        self.task_delete(self)

    def edit_clicked(self, event):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, event):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()


class App(ft.UserControl):

    def build(self):
        self.new_task = ft.TextField(hint_text="Nome da sua Tarefa", expand=True)
        self.items_left = ft.Text("0 Items ")
        self.tasks = ft.Column()

        self.filter = ft.Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="Todos"), ft.Tab(text="Ativos"), ft.Tab(text="Completos")]
        )

        self.view = ft.Column(
            width=600,
            controls=[
                ft.Row(
                    [ft.Text(value="Todos", style="headlineMedium")], alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked)
                    ]
                )
            ]
        )

        return ft.Column(
            width=600,
            controls=[
                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked),
                    ]
                ),
                ft.Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                self.items_left,
                                ft.OutlinedButton(
                                    text="Limpar Tudo", on_click=self.clear_clicked
                                )
                            ]
                        )
                    ]
                )
            ]
        )

    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                status == "Todos"
                or (status == "Ativos" and task.completed == False)
                or (status == "Completos" and task.completed)
            )
            if task.completed:
                count += 1
            self.items_left.value = f"{count} Item Completo"
        super().update()

    def task_status_change(self, task):
        self.update()

    def tabs_changed(self, event):
        self.update()

    def tabs_changed(self, event):
        self.update()

    def add_clicked(self, event):
        task = Task(self.new_task.value, self.tasks_delete, self.task_status_change)
        self.tasks.controls.append(task)
        self.new_task.value = ""
        self.update()

    def tasks_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

    def clear_clicked(self, event):
        for task in self.tasks.controls[:]:
            if task.completed:
                self.tasks_delete(task)


def main(page: ft.Page):
    page.title = "App CRUD"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()
    app1 = App()
    page.add(app1)

ft.app(target=main, view=ft.AppView.WEB_BROWSER)