import flet as ft

class Message():

    def __init__(self, user: str, text: str, message_type: str):
        self.user = user
        self.text = text
        self.message_type = message_type


class ChatMessage(ft.Row):
    
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment="start"
        self.controls=[
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user)),
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(message.user)
            ),
            ft.Column(
                [
                    ft.Text(message.user, weight="bold"),
                    ft.Text(message.text, selectable=True)
                ],
                tight=True,
                spacing=5
            ),
        ]
    
    def get_initials(self, user_name: str):
        return user_name[:1].capitalize()
    
    def get_avatar_color(self, user_name: str):
        colors_loockup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_loockup[hash(user_name) % len(colors_loockup)]

def main(page: ft.Page):
    page.title = "Chat Oscar"

    def send_message_click(e):
        if new_message.value != "":
            page.pubsub.send_all(
                Message(page.session.get("user_name"), new_message.value,
                         message_type="chat_message")
            )
            new_message.value = ""
            new_message.focus()
            page.update()

    def join_click(e):
        if not user_name.value:
            user_name.error_text = "Erro no Nome!"
            user_name.update()
        else:
            page.session.set("user_name", user_name.value)
            page.dialog.open = False
            page.pubsub.send_all(Message(
                user=user_name.value, text=f"{user_name.value} Entrou no Bate-Papo", 
                message_type="login_message")
            )
            page.update()

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            chat.controls.append(
                ft.Text(message.text, italic=True, color=ft.colors.WHITE12, size=12)
            )
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    def send_click(e):
        page.pubsub.send_all(Message(
            user=page.session.get("user_name"), text=new_message.value,
            message_type="chat_message")
        )
        new_message.value = ""
        page.update()

    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True
    )
    new_message = ft.TextField(
        hint_text="Escrevendo Messagem...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click
    )
    user_name = ft.TextField(label="Seu Nome")

    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Bem Vindo!"),
        content=ft.Column([user_name], tight=True),
        actions=[ft.ElevatedButton(text="Entrar No Bate-Papo", on_click=join_click)],
        actions_alignment="end",
    )
    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Enviar Mensagem",
                    on_click=send_message_click
                )
            ]
        )
    )

ft.app(main, view=ft.AppView.WEB_BROWSER)