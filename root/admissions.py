# Provided code
# This function checks to ensure that a list is of length
# 8 and that each element is type float
# Parameters:
# row - a list to check
# Returns True if the length of row is 8 and all elements are floats
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
	
# define your functions here
def convert_row_type(row):
    for i in range(len(row)):
        row[i] = float(row[i])
    return row

def calculate_score(row):
    return ((row[0] / 160) * 0.3) + ((row[1] * 2) * 0.4) + (row[2] * 0.1) + (row[3] * 0.2)

def is_outlier(row):
    if row[2] == 0 or ((row[1] * 2) - (row[0] / 160)) > 2:
        return True
    
def grade_outlier(row):
    sorted_row = sorted(row)
    if (sorted_row[1] - sorted_row[0]) > 20:
        return True
    
def calculate_score_improved(row):
    if calculate_score(row) >= 6  or (is_outlier(row) is True or grade_outlier is True):
        return True

def grade_improvement(row):
    if row == sorted(row):
        return True

def main():
    filename = "admission_algorithms_dataset.csv"
    
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
        headers = input_file.readline()
        print(headers)
        for line in input_file.readlines():
            new_row = []

            row = line.split(",")

            student_name = row[0]
            new_row.append(student_name) # append student name as string

            converted_row_type = convert_row_type(row[1:9]) # append all other numbers as floats
            for i in converted_row_type:
                new_row.append(i)

            if check_row_types(new_row[1:9]):
                pass
            else:
                print("ERROR: check_row_types returned a `False` value")

            # slice new_row into scores and grades
            scores = new_row[1:5]
            grades = new_row[5:9]

            calculated_score = calculate_score(scores) # passes scores into function, NOT new_row
            student_scores_file.write(f"{student_name},{calculated_score:.2f}\n")

            if calculated_score >= 6:
                chosen_students_file.write(f"{student_name}\n")

            if is_outlier(scores):
                outliers_file.write(f"{student_name}\n")

            if calculated_score >= 6 or (is_outlier(scores) and calculated_score >= 5):
                chosen_improved_file.write(f"{student_name}\n")

            if calculate_score_improved(scores):
                better_improved_file.write((','.join(map(str, new_row[0:5])) + '\n'))

            if calculated_score >= 6 or ((calculated_score >= 5) and (is_outlier(scores) or grade_outlier(grades) or grade_improvement(grades))):
                composite_chosen_file.write(f"{student_name}\n")

    print("done!")

# this bit allows us to both run the file as a program or load it as a
# module to just access the functions
if __name__ == "__main__":
    main()
