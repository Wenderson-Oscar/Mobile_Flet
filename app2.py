import flet as ft

def main(page: ft.Page):

    def register(event):
        print(name_product.value)
        print(price.value)

    page.title = 'App Test'
    txt_product = ft.Text('Nome do Produto')
    name_product = ft.TextField(label="Nome do Produto")
    txt_price = ft.Text("Preço do Produto")
    price = ft.TextField(value="0", label="Digite o Preço do Produto")
    btn_product = ft.ElevatedButton("Cadastrar", on_click=register)
    page.add(
        txt_product,
        name_product,
        txt_price,
        price,
        btn_product
    )

ft.app(target=main, view=ft.AppView.WEB_BROWSER)