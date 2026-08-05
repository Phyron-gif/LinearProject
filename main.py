from sympy import Matrix
import numpy as np
import matplotlib.pyplot as plt


#take user input for the matrix
def get_plane(plane_number):
    print(f"\nEnter the coefficients for Plane {plane_number}")
    
    a = round(float(input("Coefficient of x: ")), 2)
    b = round(float(input("Coefficient of y: ")), 2)
    c = round(float(input("Coefficient of z: ")), 2)
    d = round(float(input("Constant: ")), 2)

    return [a, b, c, d]

#call the function to get the planes
plane1 = get_plane(1)
plane2 = get_plane(2)

#build augmented matrix
augmented_matrix = Matrix([plane1, plane2])
print("\nAugmented Matrix:")
print(augmented_matrix.evalf(2))

#row reduce the augmented matrix
rref_matrix, pivot_columns = augmented_matrix.rref()
echelon_matrix = augmented_matrix.echelon_form()
print()
print("Row Echelon Form:")
print(echelon_matrix.evalf(2))
print("\nRow Reduced Echelon Form:")
print(rref_matrix.evalf(2))

print

print("\nPivot Columns:")
print(pivot_columns)

#A useful rule for this project

#Since we'll always have 2 equations and 3 variables, there are really only three outcomes:

#Inconsistent system → No solution → Parallel planes.
#Consistent system with one free variable → Infinitely many solutions → Intersection line.
#Dependent equations (one row becomes all zeros after RREF) → The two equations describe the same plane.

#analyze the RREF to determine the relationship between the planes
def analyze_rref(rref_matrix, pivot_columns):
    num_variables = rref_matrix.cols - 1  # last column is the constant/augmented column

    # Inconsistent: a pivot lands in the constant column (row like "0 = nonzero")
    if num_variables in pivot_columns:
        return "The planes are parallel and do not intersect."

    # Dependent: fewer pivots than rows means a row became all zeros
    if len(pivot_columns) < rref_matrix.rows:
        return "The planes are the same (dependent equations)."

    # Otherwise: full rank on the variables, 1 free variable -> line of intersection
    return "The planes intersect in a line."
analysis_result = analyze_rref(rref_matrix, pivot_columns)
print("\nAnalysis Result:")
print(analysis_result)

#finding the intersection line if it exists


from sympy import Matrix, symbols, simplify

def find_intersection(rref_matrix, pivot_columns):

    num_variables = rref_matrix.cols - 1

    # Variables x1, x2, x3
    variables = symbols(f"x1:{num_variables+1}")

    # Determine free columns
    free_columns = [i for i in range(num_variables)
                    if i not in pivot_columns]

    # Store the solution expressions
    solution = [None] * num_variables

    # Free variables remain themselves
    for col in free_columns:
        solution[col] = variables[col]

    # Solve pivot variables
    for row, pivot in enumerate(pivot_columns):

        expr = rref_matrix[row, -1]

        for free in free_columns:
            expr -= rref_matrix[row, free] * variables[free]

        solution[pivot] = simplify(expr)

   
    # Particular Solution
   

    particular_solution = Matrix([
        expr.subs({variables[f]: 0 for f in free_columns})
        for expr in solution
    ])

    
    # Direction Vectors
  

    direction_vectors = []

    for free in free_columns:

        direction = Matrix.zeros(num_variables, 1)

        for i, expr in enumerate(solution):

            if i == free:
                direction[i] = 1
            else:
                direction[i] = expr.coeff(variables[free])

        direction_vectors.append((variables[free], direction))

    return {
        "variables": variables,
        "pivot_columns": list(pivot_columns),
        "free_columns": free_columns,
        "solution": solution,
        "particular_solution": particular_solution,
        "direction_vectors": direction_vectors
    }

if analysis_result == "The planes intersect in a line.":
    

            result = find_intersection(rref_matrix, pivot_columns)
            print("General Solution:\n")

            print("x =")
            print(result["particular_solution"])

            for variable, direction in result["direction_vectors"]:
                print(f"\n+ {variable}")
                print(direction)
else:
     print(f"\nNo intersection line to compute since: {analysis_result}")



#visualization of the planes and their intersection line
def plot_planes(plane1, plane2, analysis_result, result=None):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Create a grid of x, y values to evaluate each plane's z
    xx, yy = np.meshgrid(np.linspace(-10, 10, 20), np.linspace(-10, 10, 20))

    def plane_z(plane, xx, yy):
        a, b, c, d = plane
        if c == 0:
            return None  # plane is vertical (parallel to z-axis), can't express as z = f(x,y)
        return (d - a * xx - b * yy) / c

    z1 = plane_z(plane1, xx, yy)
    z2 = plane_z(plane2, xx, yy)

    if z1 is not None:
        ax.plot_surface(xx, yy, z1, alpha=0.4, color='blue')
    if z2 is not None:
        ax.plot_surface(xx, yy, z2, alpha=0.4, color='red')

    # If they intersect in a line, draw it using the parametric solution
    if analysis_result == "The planes intersect in a line." and result is not None:
        t = np.linspace(-10, 10, 50)
        particular = np.array(result["particular_solution"]).astype(float).flatten()
        _, direction = result["direction_vectors"][0]
        direction = np.array(direction).astype(float).flatten()

        line_x = particular[0] + t * direction[0]
        line_y = particular[1] + t * direction[1]
        line_z = particular[2] + t * direction[2]

        ax.plot(line_x, line_y, line_z, color='green', linewidth=3, label='Intersection line')
        ax.legend()

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title(analysis_result)

    plt.savefig('planes_intersection.png')

result = plot_planes(plane1, plane2, analysis_result, result if analysis_result == "The planes intersect in a line." else None)
print("\n3D plot saved as 'planes_intersection.png'.")
    

