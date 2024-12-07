SELECT students.name, grades.grade
    FROM grades
    JOIN students ON grades.student_id = students.id
    WHERE students.group_id = ? AND grades.subject_id = ?;