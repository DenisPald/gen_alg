import tkinter as tk
from tkinter import ttk
from main import genetic_algorithm, initialize_population

class GeneticAlgorithmGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Генетический Алгоритм")

        # Заголовок
        tk.Label(root, text="Генетический Алгоритм", font=("Arial", 16)).pack(pady=10)

        # Параметры алгоритма
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(root, text="Функция 8*x1^2 + 4*x1*x2 + 5*x1^2").pack(pady=10)

        # Параметры алгоритма
        frame = tk.Frame(root)
        frame.pack(pady=10)

        # Размер популяции
        tk.Label(frame, text="Размер популяции:").grid(row=0, column=0, sticky="w")
        self.pop_size_var = tk.IntVar(value=100)
        tk.Entry(frame, textvariable=self.pop_size_var).grid(row=0, column=1)

        # Количество поколений
        tk.Label(frame, text="Количество поколений:").grid(row=1, column=0, sticky="w")
        self.generations_var = tk.IntVar(value=50)
        tk.Entry(frame, textvariable=self.generations_var).grid(row=1, column=1)

        # Вероятность мутации
        tk.Label(frame, text="Вероятность мутации (%):").grid(row=2, column=0, sticky="w")
        self.mutation_rate_var = tk.DoubleVar(value=10.0)
        tk.Entry(frame, textvariable=self.mutation_rate_var).grid(row=2, column=1)

        # Минимальное значение гена
        tk.Label(frame, text="Минимальное значение гена:").grid(row=3, column=0, sticky="w")
        self.min_gene_var = tk.DoubleVar(value=-10.0)
        tk.Entry(frame, textvariable=self.min_gene_var).grid(row=3, column=1)

        # Максимальное значение гена
        tk.Label(frame, text="Максимальное значение гена:").grid(row=4, column=0, sticky="w")
        self.max_gene_var = tk.DoubleVar(value=10.0)
        tk.Entry(frame, textvariable=self.max_gene_var).grid(row=4, column=1)

        # Метод селекции
        tk.Label(frame, text="Метод отбора родителей:").grid(row=5, column=0, sticky="w")
        self.selection_method_var = tk.StringVar(value="Панмиксия")
        tk.OptionMenu(frame, self.selection_method_var, "Панмиксия", "Ранговый отбор").grid(row=5, column=1)

        # Кнопка запуска
        tk.Button(root, text="Запустить алгоритм", command=self.run_algorithm).pack(pady=10)

        # Таблица для вывода результатов
        self.tree = ttk.Treeview(root, columns=("Generation", "Best Value", "x1", "x2"), show="headings", height=10)
        self.tree.heading("Generation", text="Поколение")
        self.tree.heading("Best Value", text="Лучшее значение")
        self.tree.heading("x1", text="x1")
        self.tree.heading("x2", text="x2")
        self.tree.pack(pady=10)
        self.tree.bind("<Control-c>", self.copy_selection)

    def copy_selection(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            clipboard_content = ""
            for item in selected_items:
                values = self.tree.item(item, "values")
                clipboard_content += str(values[1]) + "\n"
            self.root.clipboard_clear()
            self.root.clipboard_append(clipboard_content)

    def run_algorithm(self):
        # Очистка таблицы
        self.tree.delete(*self.tree.get_children())

        # Получение параметров
        pop_size = self.pop_size_var.get()
        generations = self.generations_var.get()
        mutation_rate = self.mutation_rate_var.get() / 100
        min_gene = self.min_gene_var.get()
        max_gene = self.max_gene_var.get()
        selection_method = self.selection_method_var.get()

        # Инициализация популяции
        population = initialize_population(pop_size, min_gene, max_gene)
        
        for generation in range(generations):
            best_value, best_chromosome, population = genetic_algorithm(
                population, mutation_rate, selection_method
            )
            # Добавление результатов в таблицу
            self.tree.insert("", "end", values=(generation + 1, best_value, best_chromosome[0], best_chromosome[1]))

def main():
    root = tk.Tk()
    app = GeneticAlgorithmGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
