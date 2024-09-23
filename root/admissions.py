# check length of row
def check_row_types(row):
    if len(row) != 8:
        print("Length incorrect! (should be 8): " + str(row))
        return False
    ind = 0
    while ind < len(row):
        if type(row[ind]) != float:
            print("Type of element incorrect: " + str(row[ind]) + " which is " + str(type(row[ind])))
            return False
        ind += 1
    return True
	
# convert strings to floats
def convert_row_type(row):
    for i in range(len(row)):
        row[i] = float(row[i])
    return row

# normalize sat, gpa, interest, and quality, then calculate a student score evaluation value
def calculate_score(row):
    return ((row[0] / 160) * 0.3) + ((row[1] * 2) * 0.4) + (row[2] * 0.1) + (row[3] * 0.2)

# check for interest and gpa outliers
def is_outlier(row):
    if row[2] == 0 or ((row[1] * 2) - (row[0] / 160)) > 2:
        return True

# check for bad semester outliers
def grade_outlier(row):
    sorted_row = sorted(row)
    if (sorted_row[1] - sorted_row[0]) > 20:
        return True

# determine if student is outlier
def calculate_score_improved(row):
    if calculate_score(row) >= 6  or (is_outlier(row) is True or grade_outlier is True):
        return True

# check for improving semesters
def grade_improvement(row):
    if row == sorted(row):
        return True

def main():
    # output file
    filename = "admission_algorithms_dataset.csv"
    
    # open all output files
    with (
        open(filename, "r") as input_file,
        open("better_improved.csv", "w") as better_improved_file,
        open("chosen_improved.csv", "w") as chosen_improved_file,
        open("chosen_students.csv", "w") as chosen_students_file,
        open("composite_chosen.csv", "w") as composite_chosen_file,
        open("outliers.csv", "w") as outliers_file,
        open("student_scores.csv", "w") as student_scores_file,
    ):
        
        print("Processing " + filename + "...")
        # grab headers
        headers = input_file.readline()
        print(headers)

        # one student at a time
        for line in input_file.readlines():
            new_row = []

            row = line.split(",")

            # get student name and append to list as string
            student_name = row[0]
            new_row.append(student_name) 

            # append all other numbers as floats
            converted_row_type = convert_row_type(row[1:9])
            for i in converted_row_type:
                new_row.append(i)

            # check length of row
            if check_row_types(new_row[1:9]):
                pass
            else:
                print("ERROR: check_row_types returned a `False` value")

            # slice new_row into scores and grades
            scores = new_row[1:5]
            grades = new_row[5:9]

            # calculate student score evaluation value
            calculated_score = calculate_score(scores)
            student_scores_file.write(f"{student_name},{calculated_score:.2f}\n")

            # traditionally admitted students
            if calculated_score >= 6:
                chosen_students_file.write(f"{student_name}\n")

            # interest and gpa outliers
            if is_outlier(scores):
                outliers_file.write(f"{student_name}\n")

            # admit interest and gpa outliers
            if calculated_score >= 6 or (is_outlier(scores) and calculated_score >= 5):
                chosen_improved_file.write(f"{student_name}\n")

            # bad semester outliers
            if calculate_score_improved(scores):
                better_improved_file.write((','.join(map(str, new_row[0:5])) + '\n'))

            # admit bad semester and grade improving outliers
            if calculated_score >= 6 or ((calculated_score >= 5) and (is_outlier(scores) or grade_outlier(grades) or grade_improvement(grades))):
                composite_chosen_file.write(f"{student_name}\n")

    print("done!")

if __name__ == "__main__":
    main()
