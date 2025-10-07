#
# окно с выбором в какое осно переходить
#
#-------------------------------

from tkinter import *
from product_window import ProductWindow

def SwitchWindow(auth_window):
    """Создает главное окно"""
    # Закрываем окно авторизации
    auth_window.withdraw()
    
    # Создаем главное окно
    main_win = Toplevel()
    main_win.title("Главное меню")
    main_win.geometry("800x600")
    
    # Контент главного окна
    Label(main_win, text="Добро пожаловать!", font=("Arial", 20)).pack(pady=50)
    
    def switch():
        ProductWindow(main_win)

    Button(main_win, text="Продукты", command=lambda: switch()).pack()

    # Кнопка выхода
    Button(main_win, text="Выйти", 
           command=lambda: exit_app(main_win, auth_window)).pack()

def exit_app(main_window, auth_window):
    """Выход из приложения"""
    main_window.destroy()
    auth_window.destroy()

