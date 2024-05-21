from problemSolver.ProblemSolver import ProblemSolver
from problems.FindTheIndex import FindTheIndex

def main():
    """
    Main function to run the application.
    This is the entry point.
    """
    problem = FindTheIndex()
    solver = ProblemSolver(problem)
    solver.findTheIndex()

if __name__ == '__main__':
    main()