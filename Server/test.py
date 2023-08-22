from service import TeacherService

service = TeacherService()

student = service.students[0]
student.name = "302"

finded_student = service.find_student_by_index(2)

print(student)
print(finded_student)