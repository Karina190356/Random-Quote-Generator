import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import List, Dict, Any, Optional

# Попытка импортировать ttkthemes для стилизации. Если не получится, используем стандартный ttk.
try:
    import ttkthemes as themes
    THEMES_AVAILABLE = True
except ImportError:
    print("Библиотека ttkthemes не найдена. Используется стандартный стиль Tk.")
    THEMES_AVAILABLE = False

from quote_manager import (
    load_quotes,
    save_quotes,
    init_data_file,
    get_random_quote,
    add_quote,
    filter_quotes_by_author,
    filter_quotes_by_topic,
    get_unique_authors,
    get_unique_topics
)


class QuoteGeneratorApp:
    """
    Главное приложение для генерации случайных цитат с графическим интерфейсом.
    """
    def __init__(self, root: tk.Tk):
        """
        Инициализирует приложение и создает все виджеты.
        :param root: Корневой элемент Tkinter (Tk или ThemedTk).
        """
        self.root = root
        self.root.title("Генератор случайных цитат")
        self.root.geometry("700x500")
        
        # Инициализация данных и истории
        init_data_file()
        self.quotes: List[Dict[str, Any]] = load_quotes()
        self.history: List[Dict[str, Any]] = []
        
        self.create_widgets()
        self.update_history_display()
        
        # Заполняем фильтры уникальными значениями из базы данных
        self.update_filter_options()

    def create_widgets(self) -> None:
        """Создает все элементы графического интерфейса."""
        # --- Основной фрейм для цитаты ---
        quote_frame = ttk.LabelFrame(self.root, text="Случайная цитата")
        quote_frame.pack(pady=10, fill='x', padx=10)

        self.quote_text = tk.StringVar()
        self.quote_author = tk.StringVar()
        self.quote_topic = tk.StringVar()

        ttk.Label(quote_frame, textvariable=self.quote_text, wraplength=500, font=("Arial", 12)).pack(pady=5)
        ttk.Label(quote_frame, textvariable=self.quote_author, font=("Arial", 10, "italic")).pack()
        ttk.Label(quote_frame, textvariable=self.quote_topic, font=("Arial", 10)).pack()

        ttk.Button(quote_frame, text="Сгенерировать цитату", command=self.generate_quote).pack(pady=10)


        # --- Фрейм для добавления новой цитаты ---
        add_frame = ttk.LabelFrame(self.root, text="Добавить свою цитату")
        add_frame.pack(pady=10, fill='x', padx=10)
        
        ttk.Button(add_frame, text="Добавить цитату", command=self.add_new_quote_dialog).pack()


        # --- Фрейм для фильтрации ---
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация истории")
        filter_frame.pack(pady=10, fill='x', padx=10)
        
        # Фильтр по автору
        self.author_var = tk.StringVar()
        self.author_combobox = ttk.Combobox(filter_frame, textvariable=self.author_var, state='readonly')
        self.author_combobox.pack(side='left', padx=5)
        
        ttk.Button(filter_frame, text="Фильтр по автору", command=self.filter_by_author).pack(side='left', padx=5)
        
        # Фильтр по теме
        self.topic_var = tk.StringVar()
        self.topic_combobox = ttk.Combobox(filter_frame, textvariable=self.topic_var, state='readonly')
        self.topic_combobox.pack(side='left', padx=5)
        
        ttk.Button(filter_frame, text="Фильтр по теме", command=self.filter_by_topic).pack(side='left', padx=5)
        
        # Кнопка сброса фильтра
        ttk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter).pack(side='left', padx=5)


        # --- Фрейм для истории ---
        history_frame = ttk.LabelFrame(self.root, text="История сгенерированных цитат")
        history_frame.pack(pady=10, fill='both', expand=True, padx=10)
        
        self.history_listbox = tk.Listbox(history_frame, height=10)
        self.history_listbox.pack(fill='both', expand=True)


    def update_filter_options(self) -> None:
        """Обновляет списки авторов и тем для фильтрации."""
        authors = get_unique_authors(self.quotes)
        topics = get_unique_topics(self.quotes)
        
        self.author_combobox['values'] = authors
        self.topic_combobox['values'] = topics

    def generate_quote(self) -> None:
        """Генерирует и отображает случайную цитату."""
        if not self.quotes:
            messagebox.showwarning("Предупреждение", "База данных цитат пуста. Добавьте свои цитаты!")
            return

        quote = get_random_quote(self.quotes)
        
        if quote:
            self.quote_text.set(quote.get('text', '—'))
            self.quote_author.set(f"— {quote.get('author', 'Неизвестный автор')}")
            self.quote_topic.set(f"Тема: {quote.get('topic', 'Без темы')}")
            
            # Добавляем в историю и сохраняем её
            self.history.append(quote)
            save_quotes(self.history)  # Сохраняем только историю в отдельный файл или тот же?
            self.update_history_display()

    def update_history_display(self) -> None:
        """Обновляет виджет списка истории."""
        self.history_listbox.delete(0, tk.END)
        
        if not self.history:
            self.history_listbox.insert(tk.END, "История пуста.")
            return

        for i, quote in enumerate(self.history):
            entry = f"{i+1}. «{quote.get('text', '')}» — {quote.get('author', '')}"
            self.history_listbox.insert(tk.END, entry)

    def add_new_quote_dialog(self) -> None:
        """Открывает диалоговое окно для добавления новой цитаты."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить новую цитату")
        dialog.geometry("400x250")
        
         # --- Поля ввода ---
         fields = {}
         labels = ["Текст цитаты:", "Автор:", "Тема:"]
         variables = [tk.StringVar(), tk.StringVar(), tk.StringVar()]
         
         for idx, (label_text, var) in enumerate(zip(labels, variables)):
             frame = ttk.Frame(dialog)
             frame.pack(pady=5, fill='x', padx=10)
             
             ttk.Label(frame, text=label_text, width=15).pack(side='left')
             entry = ttk.Entry(frame, textvariable=var, width=30)
             entry.pack(side='left', expand=True, fill='x')
             fields[label_text] = entry

         def on_submit() -> None:
             """Обрабатывает отправку формы."""
             text = fields["Текст цитаты:"].get().strip()
             author = fields["Автор:"].get().strip()
             topic = fields["Тема:"].get().strip()
             
             if not text or not author:
                 messagebox.showerror("Ошибка", "Поля 'Текст' и 'Автор' обязательны для заполнения!")
                 return

             try:
                 add_quote(text=text, author=author, topic=topic)
                 messagebox.showinfo("Успех", "Цитата успешно добавлена в базу данных!")
                 dialog.destroy()
                 
                 # Обновляем фильтры и базу данных в памяти
                 self.quotes = load_quotes()
                 self.update_filter_options()
                 
             except Exception as e:
                 messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить цитату: {e}")
         
         submit_btn = ttk.Button(dialog, text="Добавить", command=on_submit)
         submit_btn.pack(pady=15)

    def filter_by_author(self) -> None:
        """Фильтрует историю по выбранному автору."""
         author = self.author_var.get()
         if not author:
             return
         
         filtered_history = filter_quotes_by_author(self.history, author)
         self.display_filtered_history(filtered_history)

    def filter_by_topic(self) -> None:
         """Фильтрует историю по выбранной теме."""
         topic = self.topic_var.get()
         if not topic:
             return
         
         filtered_history = filter_quotes_by_topic(self.history, topic)
         self.display_filtered_history(filtered_history)

    def display_filtered_history(self, filtered_list: List[Dict[str, Any]]) -> None:
         """Отображает отфильтрованный список в виджете."""
         self.history_listbox.delete(0, tk.END)
         
         if not filtered_list:
             self.history_listbox.insert(tk.END, "По вашему запросу ничего не найдено.")
             return

         for i, quote in enumerate(filtered_list):
             entry = f"{i+1}. «{quote.get('text', '')}» — {quote.get('author', '')}"
             self.history_listbox.insert(tk.END, entry)

    def reset_filter(self) -> None:
         """Сбрасывает фильтр и показывает полную историю."""
         self.update_history_display()


# --- Точка входа ---
if __name__ == "__main__":
    try:
         if 'THEMES_AVAILABLE' in globals() and THEMES_AVAILABLE:
              root = themes.ThemedTk()
              app = QuoteGeneratorApp(root)  # Передаем уже созданный root
              root.mainloop()
         else:
              root = tk.Tk()  # Если нет — обычный Tk.
              app = QuoteGeneratorApp(root)  # Передаем уже созданный root
              root.mainloop()
    except NameError:
          root = tk.Tk()
          app = QuoteGeneratorApp(root)
          root.mainloop()
