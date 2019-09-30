# Team members: Cameron Storton, Zachary Richardson, Weston Gilmore

STLASTNAME = 0
STFIRSTNAME = 1
GRADE = 2
CLASSROOM = 3
BUS = 4
GPA = 5

TLASTNAME = 0
TFIRSTNAME = 1
TCLASSROOM = 2

NUM_GRADES = 7

from collections import defaultdict

def main():
    students = get_file_as_array("list.txt")
    teachers = get_file_as_array("teachers.txt")

    inp = get_user_input()
    while inp not in ["Q", "QUIT"]:
        split_inp = inp.strip().split(":")
        
        if len(split_inp) is not 2:
            if split_inp[0] in ["I", "INFO"]:
                i_query(students)
            else:
                print_bad_query_msg()
        else:
            query_type = split_inp[0]
            query_args = split_inp[1].strip().split(" ")
            parse_query(query_type, query_args, students, teachers)

        inp = get_user_input()

def parse_query(query_type, query_args, students, teachers):
    query_type_dict={
        "S":s_query,
        "STUDENT":s_query,
        "T":t_query,
        "TEACHER":t_query,
        "B":b_query,
        "BUS":b_query,
        "G":g_query,
        "GRADE":g_query,
        "A":a_query,
        "AVERAGE":a_query,
        "C":c_query,
        "CLASSROOM":c_query
    }
    parsing_function = query_type_dict.get(query_type, print_bad_query_msg)
    parsing_function(query_args, students, teachers)

def s_query(query_args, students, teachers):
    if len(query_args) is 1:
        last_name = query_args[0]
        for student in students:
            if student[0] == last_name:
                teachers = get_teachers_by_classroom(teachers, student[CLASSROOM])
                print("%s, %s, %s, %s, %s, %s"
                    % (student[STLASTNAME], student[STFIRSTNAME],
                    student[GRADE], student[CLASSROOM], teachers[0][TLASTNAME],
                    teachers[0][TFIRSTNAME]))
    elif len(query_args) is 2 and query_args[1] is ("B" or "BUS"):
        last_name = query_args[0]
        for student in students:
            if student[STLASTNAME] == last_name:
                print("%s, %s, %s"
                    % (student[STLASTNAME], student[STFIRSTNAME], student[BUS]))
    else:
        print_bad_query_msg()

def t_query(query_args, students, teachers):
    if len(query_args) is not 1:
        print_bad_query_msg()

    last_name = query_args[0]
    for student in students:
        if student[TLASTNAME] == last_name:
            print("%s, %s" % (student[STLASTNAME], student[STFIRSTNAME]))

def b_query(query_args, students, teachers):
    if len(query_args) is not 1:
        print_bad_query_msg()
    try:
        bus = int(query_args[0])
        for student in students:
            if int(student[BUS]) == bus:
                print("%s, %s, %s, %s"
                    % (student[STLASTNAME], student[STFIRSTNAME], student[GRADE],
                    student[CLASSROOM]))
    except ValueError:
        print("B[us] takes a valid integer, not %s" % (query_args[0]))
        print_bad_query_msg()

def g_query(query_args, students, teachers):
    try:
        if len(query_args) is 1:
            grade = int(query_args[0])
            for student in students:
                if int(student[GRADE]) == grade:
                    print("%s, %s" % (student[STLASTNAME], student[STFIRSTNAME]))
        elif len(query_args) is 2:
            grade = int(query_args[0])
            if query_args[1] is ("H" or "HIGH"):
                highest_gpa = 0.0
                top_student = None
                for student in students:
                    if int(student[GRADE]) == grade:
                        if float(student[GPA]) >= highest_gpa:
                            highest_gpa = float(student[GPA])
                            top_student = student
                if top_student:
                    teachers = get_teachers_by_classroom(teachers, top_student[CLASSROOM])
                    print("%s, %s, %.2f, %s, %s, %s"
                        % (top_student[STLASTNAME], top_student[STFIRSTNAME],
                        highest_gpa, teachers[0][TLASTNAME], teachers[0][TFIRSTNAME],
                        top_student[BUS]))
            elif query_args[1] is ("L" or "LOW"):
                lowest_gpa = float(4.0)
                worst_student = None
                for student in students:
                    if int(student[GRADE]) == grade:
                        if float(student[GPA]) <= lowest_gpa:
                            lowest_gpa = float(student[GPA])
                            worst_student = student
                if worst_student:
                    teacher = get_teacher_by_classroom(teachers, worst_student[CLASSROOM])
                    print("%s, %s, %.2f, %s, %s, %s"
                        % (worst_student[STLASTNAME], worst_student[STFIRSTNAME],
                        lowest_gpa, teacher[TLASTNAME],
                        teacher[TFIRSTNAME], worst_student[BUS]))
            else:
                print_bad_query_msg()
        else:
            print_bad_query_msg()
    except ValueError:
        print("G[rade] takes a valid integer, not %s" % (query_args[0]))
        print_bad_query_msg()


def a_query(query_args, students, teachers):
    if len(query_args) is not 1:
        print_bad_query_msg()

    num_gpas = 0
    gpa_sum = 0.0
    try:
        grade = int(query_args[0])
        for student in students:
            if int(student[GRADE]) == grade:
                num_gpas+= 1
                gpa_sum += float(student[GPA])
        average_gpa = gpa_sum / num_gpas if num_gpas > 0 else 0.0
        print("%d, %.2f" % (grade, average_gpa))
    except ValueError:
        print("A[verage] takes a valid integer, not %s" % (query_args[0]))
        print_bad_query_msg()

def i_query(students):
    total_students = 0
    grade_array = [0] * NUM_GRADES
    for student in students:
        try:
            grade_array[int(student[GRADE])] += 1
        except ValueError:
            print("I[nfo] found a student with an invalid grade:")
            print(student)
    for grade in range(NUM_GRADES):
        print("%d: %d" % (grade, grade_array[grade]))

def c_query(query_args, students, teachers):
    print("TODO")

def print_bad_query_msg(*args):
    print("Usage:")
    print("  S[tudent]: <lastname> [B[us]]")
    print("  T[eacher]: <lastname>")
    print("  B[us]: <number>")
    print("  G[rade]: <number> [H[igh]|L[ow]]")
    print("  A[verage]: <number>")
    print("  I[nfo]")
    print("  Q[uit]")

def get_user_input():
    return input("$ ").upper()

def get_teachers_by_classroom(teachers, classroom):
    res = []
    for teacher in teachers:
        if teacher[TCLASSROOM] == classroom:
            res.append(teacher)
    if len(res) is 0:
        print("No teachers found for given classroom!")
    else:
        return res

def get_file_as_array(filename):
    try:
        _file = open(filename, "r")
        entry_array = []
        for line in _file.readlines():
            entry_array.append(line.strip().split(","))
            for num in range(len(entry_array[-1])):
                entry_array[-1][num] = entry_array[-1][num].strip()
        return entry_array
    # Catch file not found
    except OSError as e:
        print("''" + filename + " not found in the current directory.")
        exit(1)

if __name__ == "__main__":
    main()
