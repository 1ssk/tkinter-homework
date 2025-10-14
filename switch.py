#
# окно с выбором в какое окно переходить sales.py
#
#-------------------------------

from tkinter import *
from product import ProductWindow
from sales import SalesWindow
from partner import PartnerWindow

def SwitchWindow(auth):
    """Главное меню"""
    auth.withdraw()  # скрываем окно авторизации

    switch = Toplevel()
    switch.title("Главное меню")
    switch.geometry("600x400")
    switch.configure(bg="#FFF8DC")

    Label(switch, text="Добро пожаловать!", 
          font=("Arial", 18, "bold"), bg="#FFF8DC").pack(pady=(30, 20))

    Label(switch, text="Выберите раздел:", 
          font=("Arial", 12), bg="#FFF8DC").pack(pady=(0, 15))

    # Фрейм для кнопок
    btn_frame = Frame(switch, bg="#FFF8DC")
    btn_frame.pack(pady=20)

    def create_btn(text, command):
        return Button(btn_frame, text=text, command=command,
                      bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                      width=20, padx=5, pady=5, relief="flat", cursor="hand2")

    create_btn("Продукция", lambda: ProductWindow()).pack(pady=8)
    create_btn("Продажи", lambda: SalesWindow()).pack(pady=8)
    create_btn("Партнеры", lambda: PartnerWindow()).pack(pady=8)

    # Кнопка выхода
    Button(switch, text="Выйти", command=switch.destroy,
           bg="#F44336", fg="white", font=("Arial", 10, "bold"),
           width=10, padx=4, pady=4, relief="flat", cursor="hand2").pack(pady=20)





