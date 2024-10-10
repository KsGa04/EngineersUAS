# Схема базы данных

## Table: `users`
### Таблица "Пользователи" предназначена для хранения информации о студентах/выпускниках
| Column Name       | Data Type                                   | Constraints                         |
|-------------------|---------------------------------------------|-------------------------------------|
| id                | INT                                         | AUTO_INCREMENT, PRIMARY KEY         |
| email             | VARCHAR(255)                                | UNIQUE, NOT NULL                    |
| password          | VARCHAR(255)                                | NOT NULL                            |
| role              | ENUM('student', 'employer', 'UEM', 'admin') | NOT NULL                            |
| first_name        | VARCHAR(100)                                | NOT NULL                            |
| last_name         | VARCHAR(100)                                | NOT NULL                            |
| phone             | VARCHAR(20)                                 |                                     |
| telegram_username | VARCHAR(50)                                 |                                     |
| city              | VARCHAR(255)                                |                                     |
| image             | BLOB                                        |                                     |
| created_at        | TIMESTAMP                                   | DEFAULT CURRENT_TIMESTAMP           |
| updated_at        | TIMESTAMP                                   | DEFAULT CURRENT_TIMESTAMP ON UPDATE |

---

## Table: `universities`
### Таблица "Университет" предназначена для хранения информации об университетах пользователи которых имеются в бд
| Column Name | Data Type    | Constraints                         |
|-------------|--------------|-------------------------------------|
| id          | INT          | AUTO_INCREMENT, PRIMARY KEY         |
| name        | VARCHAR(255) | NOT NULL                            |
| city        | VARCHAR(255) | NOT NULL                            |
| created_at  | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP           |
| updated_at  | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP ON UPDATE |

---

## Table: `specialties`
### Таблица "Специальности/направления" предназначена для хранения информации о направлениях в университете
| Column Name   | Data Type    | Constraints                                               |
|---------------|--------------|-----------------------------------------------------------|
| id            | INT          | AUTO_INCREMENT, PRIMARY KEY                               |
| name          | VARCHAR(255) | NOT NULL                                                  |
| university_id | INT          | FOREIGN KEY REFERENCES universities(id) ON DELETE CASCADE |
| created_at    | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP                                 |
| updated_at    | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP ON UPDATE                       |

---

## Table: `groups`
### Таблица "Группы" предназначена для хранения информации о группах в университете
| Column Name  | Data Type   | Constraints                                              |
|--------------|-------------|----------------------------------------------------------|
| id           | INT         | AUTO_INCREMENT, PRIMARY KEY                              |
| group_number | VARCHAR(50) | NOT NULL                                                 |
| specialty_id | INT         | FOREIGN KEY REFERENCES specialties(id) ON DELETE CASCADE |
| created_at   | TIMESTAMP   | DEFAULT CURRENT_TIMESTAMP                                |
| updated_at   | TIMESTAMP   | DEFAULT CURRENT_TIMESTAMP ON UPDATE                      |

---

## Table: `assignments`
### Таблица "Задания" предназначена для хранения информации о заданиях, которые выполняют студенты на своих направлениях
| Column Name | Data Type                            | Constraints                                         |
|-------------|--------------------------------------|-----------------------------------------------------|
| id          | INT                                  | AUTO_INCREMENT, PRIMARY KEY                         |
| title       | VARCHAR(255)                         | NOT NULL                                            |
| description | TEXT                                 |                                                     |
| group_id    | INT                                  | FOREIGN KEY REFERENCES groups(id) ON DELETE CASCADE |
| type        | ENUM('lab', 'coursework', 'diploma') | NOT NULL                                            |
| created_at  | TIMESTAMP                            | DEFAULT CURRENT_TIMESTAMP                           |
| updated_at  | TIMESTAMP                            | DEFAULT CURRENT_TIMESTAMP ON UPDATE                 |

---

## Table: `skills`
### Таблица "Навыки" предназначена для хранения информации о навыках
| Column Name         | Data Type                   | Constraints                        |
|---------------------|-----------------------------|------------------------------------|
| id                  | INT                         | AUTO_INCREMENT, PRIMARY KEY        |
| name                | VARCHAR(255)                | NOT NULL                           |
| created_at          | TIMESTAMP                   | DEFAULT CURRENT_TIMESTAMP          |

---

## Table: `assignment_skills`
### Таблица "Задания_навыки" смежная таблица между "Заданиями" и "Навыками". Т.к под каждым заданием должны указываться навыки, которые были необходимы для выполнения задания
| Column Name   | Data Type | Constraints                                              |
|---------------|-----------|----------------------------------------------------------|
| id            | INT       | AUTO_INCREMENT, PRIMARY KEY                              |
| assignment_id | INT       | FOREIGN KEY REFERENCES assignments(id) ON DELETE CASCADE |
| skill_id      | INT       | FOREIGN KEY REFERENCES skills(id) ON DELETE CASCADE      |

---

## Table: `user_groups`
### Таблица "Студенты_группы" смежная таблица между "Пользователями" и "Группами". Т.к студент может как закончить к примеру бакалавриат, так и уже обучаться в магистратуре
| Column Name | Data Type | Constraints                                         |
|-------------|-----------|-----------------------------------------------------|
| id          | INT       | AUTO_INCREMENT, PRIMARY KEY                         |
| user_id     | INT       | FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE  |
| group_id    | INT       | FOREIGN KEY REFERENCES groups(id) ON DELETE CASCADE |

---

## Table: `resumes`
### Таблица "Резюме" предназначена для хранения информации о резюме пользователя
| Column Name         | Data Type    | Constraints                                               |
|---------------------|--------------|-----------------------------------------------------------|
| id                  | INT          | AUTO_INCREMENT, PRIMARY KEY                               |
| user_id             | INT          | FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE        |
| university_id       | INT          | FOREIGN KEY REFERENCES universities(id) ON DELETE CASCADE |
| specialty_id        | INT          | FOREIGN KEY REFERENCES specialties(id) ON DELETE CASCADE  |
| group_id            | INT          | FOREIGN KEY REFERENCES groups(id) ON DELETE CASCADE       |
| title               | VARCHAR(255) |                                                           |
| summary             | TEXT         |                                                           |
| project_description | TEXT         | Описание проектов (дипломы, лабораторные задания)         |
| results             | TEXT         | Конечный результат работы                                 |
| personal_projects   | TEXT         | Персональные проекты (pet-проекты)                        |
| portfolio_links     | TEXT         | Ссылки на GitHub или примеры работ                        |
| created_at          | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP                                 |
| updated_at          | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP ON UPDATE                       |

---

## Table: `resume_skills`
### Таблица "Резюме_навыки" смежная таблица между "Резюме" и "Навыками". Т.к пользователь может владеть множеством навыков, и также этими навыками может владеть другой пользователь
| Column Name | Data Type | Constraints                                          |
|-------------|-----------|------------------------------------------------------|
| id          | INT       | AUTO_INCREMENT, PRIMARY KEY                          |
| resume_id   | INT       | FOREIGN KEY REFERENCES resumes(id) ON DELETE CASCADE |
| skill_id    | INT       | FOREIGN KEY REFERENCES skills(id) ON DELETE CASCADE  |

---

## Table: `languages`
### Таблица "Языки" предназначена для хранения информации о языках
| Column Name         | Data Type                   | Constraints                        |
|---------------------|-----------------------------|------------------------------------|
| id                  | INT                         | AUTO_INCREMENT, PRIMARY KEY        |
| name                | VARCHAR(255)                | NOT NULL                           |
| created_at          | TIMESTAMP                   | DEFAULT CURRENT_TIMESTAMP          |

---

## Table: `resume_languages`
### Таблица "Резюме_языки" смежная таблица между "Резюме" и "Языки". Т.к пользователь может владеть множеством навыков, и также этими навыками может владеть другой пользователь
| Column Name       | Data Type                                              | Constraints                                            |
|-------------------|--------------------------------------------------------|--------------------------------------------------------|
| id                | INT                                                    | AUTO_INCREMENT, PRIMARY KEY                            |
| resume_id         | INT                                                    | FOREIGN KEY REFERENCES resumes(id) ON DELETE CASCADE   |
| language_id       | INT                                                    | FOREIGN KEY REFERENCES languages(id) ON DELETE CASCADE |
| proficiency_level | ENUM('beginner', 'intermediate', 'advanced', 'fluent') | NOT NULL                                               |

---

## Table: `jobs`
### Таблица "Вакансии" предназначена для хранения информации о вакансиях
| Column Name  | Data Type    | Constraints                                        |
|--------------|--------------|----------------------------------------------------|
| id           | INT          | AUTO_INCREMENT, PRIMARY KEY                        |
| employer_id  | INT          | FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE |
| title        | VARCHAR(255) |                                                    |
| description  | TEXT         |                                                    |
| requirements | TEXT         |                                                    |
| location     | VARCHAR(255) | Регион публикации вакансии                         |
| salary_range | VARCHAR(50)  | Уровень заработной платы                           |
| specialty    | VARCHAR(255) | Специальность или должность                        |
| created_at   | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP                          |
| updated_at   | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP ON UPDATE                |

---

## Table: `job_applications`
### Таблица "Отклики" смежная таблица между "Вакансиями" и "Пользователями". Т.к пользователь может откликнуться на множество вакансий, и также на одну вакансию может быть множество откликов
| Column Name | Data Type                                           | Constraints                                          |
|-------------|-----------------------------------------------------|------------------------------------------------------|
| id          | INT                                                 | AUTO_INCREMENT, PRIMARY KEY                          |
| user_id     | INT                                                 | FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE   |
| job_id      | INT                                                 | FOREIGN KEY REFERENCES jobs(id) ON DELETE CASCADE    |
| resume_id   | INT                                                 | FOREIGN KEY REFERENCES resumes(id) ON DELETE CASCADE |
| status      | ENUM('pending', 'reviewed', 'accepted', 'rejected') | DEFAULT 'pending'                                    |
| applied_at  | TIMESTAMP                                           | DEFAULT CURRENT_TIMESTAMP                            |

---

## Table: `job_skills`
### Таблица "Вакансии_навыки" смежная таблица между "Вакансии" и "Навыками". Т.к на одну вакансию может требоваться несколько навыков, и один навык может требоваться на множество вакансию
| Column Name | Data Type | Constraints                                         |
|-------------|-----------|-----------------------------------------------------|
| id          | INT       | AUTO_INCREMENT, PRIMARY KEY                         |
| job_id      | INT       | FOREIGN KEY REFERENCES jobs(id) ON DELETE CASCADE   |
| skill_id    | INT       | FOREIGN KEY REFERENCES skills(id) ON DELETE CASCADE |

---

## Table: `sessions`
### Таблица "Сессии" предназначена для хранения информации о посещаемости пользователей
| Column Name | Data Type    | Constraints                                        |
|-------------|--------------|----------------------------------------------------|
| user_id     | INT          | FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE |
| token       | VARCHAR(255) | UNIQUE, NOT NULL                                   |
| created_at  | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP                          |
| deadline_at | TIMESTAMP    | NULL                                               |

---

## Table: `notifications`
### Таблица "Уведомления" предназначена для хранения информации о уведомлениях пользователей
| Column Name | Data Type | Constraints                                        |
|-------------|-----------|----------------------------------------------------|
| user_id     | INT       | FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE |
| content     | TEXT      | NOT NULL                                           |
| sent_at     | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP                          |
