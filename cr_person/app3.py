import flet as ft
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

""" DATABASE """

CONN = "sqlite:///project.db"

engine = create_engine(CONN, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Product(Base):
    __tablename__ = "product" 
    id = Column(String(50), primary_key=True)
    title = Column(String(50))
    price = Column(Float)
Base.metadata.create_all(engine)

""" MOBILE """

def main(page: ft.Page):

    list_product = ft.ListView()

    def register(event):
        try:
            new_product = Product(id=str(uuid.uuid4()), title=name_product.value, price=price.value)
            session.add(new_product)
            session.commit()
            list_product.controls.append(
                ft.Container(
                    ft.Text(name_product.value),
                    bgcolor=ft.colors.BLACK12,
                    padding=15,
                    alignment=ft.alignment.center,
                    margin=3,
                    border_radius=10,
                )
            )
            txt_error.visible = False
            txt_asser.visible = True
        except:
            txt_error.visible = True
            txt_asser.visible = False
        page.update()
        print('Produto Cadastrado')

    txt_error = ft.Container(ft.Text("Erro ao Salvar o Produto!"), visible=False, bgcolor=ft.colors.RED, padding=10, alignment=ft.alignment.center)
    txt_asser = ft.Container(ft.Text("Produto Salvo com Sucesso"), visible=False, bgcolor=ft.colors.GREEN, padding=10, alignment=ft.alignment.center)

    page.title = 'App Test'
    txt_product = ft.Text('Nome do Produto')
    name_product = ft.TextField(label="Nome do Produto")
    txt_price = ft.Text("Preço do Produto")
    price = ft.TextField(value="0", label="Digite o Preço do Produto")
    btn_product = ft.ElevatedButton("Cadastrar", on_click=register)

    page.add(
        txt_error,
        txt_asser,
        txt_product,
        name_product,
        txt_price,
        price,
        btn_product
    )

    for pr in session.query(Product).all():
        list_product.controls.append(
            ft.Container(
                ft.Text(pr.title),
                bgcolor=ft.colors.BLACK12,
                padding=15,
                alignment=ft.alignment.center,
                margin=3,
                border_radius=10,
            )
        )
    page.add(
        list_product,
    )

ft.app(target=main, view=ft.AppView.WEB_BROWSER)