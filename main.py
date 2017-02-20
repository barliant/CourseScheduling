from Course import Course, CoursesGraph
from scheduling import *
from loadData import DataLoading

creditsPerQuarter = 16

# data loading
## for Computer Science graph
SpecsCourse, SpecsTable = DataLoading().loadSpec(major="Computer Science",
                                                 specs=["Lower-division", "Upper-division","Writing","Intelligent Systems"],
                                                 filename="info/test/specializations.txt")
graph = CoursesGraph()
DataLoading().loadCourses(graph, "info/test/fullcourses.txt")
# DataLoading().loadCourses(graph, "info/test/noprereq.txt")
graph.updateSatisfies()
graph.loadSpecs(SpecsCourse)

## ge graph
geGraph = CoursesGraph()
DataLoading().loadCourses(geGraph, "info/test/ge.txt")
generalCourse, generalSpecsTable = DataLoading().loadSpec(major="General",
                                                          specs=["GEII", "GEIV", "GEV", "GEVI"],
                                                          filename="info/test/general.txt")

geGraph.loadSpecs(generalCourse)
SpecsTable.update(generalSpecsTable)

# scheduling
L, bestBound = CourseScheduling([graph,geGraph], SpecsTable, creditsPerQuarter).findBestSchedule(5)

print("Taking %d credits per quarter: " % (creditsPerQuarter))
for i, level in enumerate(L):
	print("year %d quarter %d:" % (i // 3 + 1, i % 3 + 1), level)

print(bestBound)
"""
Taking 16 credits per quarter:
year 1 quarter 1: ['WRITING39A', 'MATH2A', 'I&CSCI90', 'I&CSCI31']
year 1 quarter 2: ['I&CSCI6B', 'WRITING39B', 'MATH2B', 'IN4MATX131']
year 1 quarter 3: ['I&CSCI32', 'I&CSCI51', 'I&CSCI6D']
year 2 quarter 1: ['WRITING39C', 'STATS67', 'MATH3A', 'I&CSCI33']
year 2 quarter 2: ['I&CSCI53+53L', 'COMPSCI178', 'I&CSCI45C']
year 2 quarter 3: ['IN4MATX43', 'COMPSCI132', 'COMPSCI177', 'COMPSCI122A']
year 3 quarter 1: ['COMPSCI184A', 'COMPSCI169', 'COMPSCI151', 'I&CSCI46']
year 3 quarter 2: ['I&CSCI139W', 'COMPSCI125', 'IN4MATX113', 'COMPSCI133']
year 3 quarter 3: ['COMPSCI154', 'GEIV-3', 'GEVIII-1', 'GEII-2']
year 4 quarter 1: ['IN4MATX121', 'COMPSCI161', 'COMPSCI171', 'GEIV-2']
year 4 quarter 2: ['COMPSCI175', 'GEII-1', 'GEVI-1', 'GEVII-1']
year 4 quarter 3: ['GEIV-1']
7
"""
