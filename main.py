import numpy as np

# Функция для вычисления целевой функции
def objective_function(x):
    return 8 * x[0]**2 + 4 * x[0] * x[1] + 5 * x[1]**2

# Генерация начальной популяции
def initialize_population(size, min_gene, max_gene):
    return np.random.uniform(min_gene, max_gene, (size, 2))

# Селекция методом Пропорционального отбора
def selection(population, selection_size):
    # Вычисляем приспособленность каждого индивида
    fitness_values = np.array([1/objective_function(ind) for ind in population])

    # Преобразуем приспособленность в вероятности (нормализуем)
    fitness_sum = np.sum(fitness_values)
    probabilities = fitness_values / fitness_sum

    # Выбираем индивидов на основе вероятностей
    selected_indices = np.random.choice(len(population), size=selection_size, p=probabilities)
    selected = population[selected_indices]

    return selected

# Выбор родителей методами панмиксии или рангового отбора
def select_parents(population, probabilities, select_parents_type):
    if select_parents_type == "Панмиксия":
        indices = np.random.choice(len(population), size=2, replace=False)
        return population[indices]
    elif select_parents_type == "Ранговый отбор":
        # Выбор двух родителей с вероятностями, пропорциональными рангу
        selected_indices = np.random.choice(len(population), size=2, replace=False, p=probabilities)
        return population[selected_indices]
    else:
        raise ValueError(f"Некорректный тип отбора родителей: {select_parents_type}")

# Мутация
def mutate(offspring, mutation_rate):
    if np.random.rand() < mutation_rate:
        offspring += np.random.uniform(-0.1, 0.1, 2)
    return offspring

# Кроссинговер методом простого среднего
def crossover(parent1, parent2):
    return (parent1 + parent2) / 2

# Вычисление рангов для рангового отбора
def calculate_rank_probabilities(population):
    fitness_scores = np.array([1/objective_function(ind) for ind in population])
    sorted_indices = np.argsort(fitness_scores)  # Сортировка по возрастанию значений функции (лучшие в начале)
    
    # Присвоение рангов: лучший индивид получает ранг len(population), худший — 1
    ranks = np.zeros_like(fitness_scores, dtype=float)
    for rank, idx in enumerate(sorted_indices, start=1):
        ranks[idx] = rank**2
    
    # Конвертация рангов в вероятности
    probabilities = ranks / np.sum(ranks)
    return probabilities

# Основная функция генетического алгоритма
def genetic_algorithm(population, mutation_rate, select_parents_type, selection_size):
    # Селекция
    new_population = selection(population, selection_size)

    probabilities = calculate_rank_probabilities(population)

    while len(new_population) < len(population):
        parents = select_parents(population, probabilities, select_parents_type)
        child = crossover(*parents)
        child = mutate(child, mutation_rate)
        new_population = np.vstack([new_population, child])

    # Найти лучшее решение
    fitness_scores = np.array([objective_function(ind) for ind in new_population])
    best_index = np.argmin(fitness_scores)
    best_value = fitness_scores[best_index]
    best_chromosome = new_population[best_index]

    return best_value, best_chromosome, new_population
