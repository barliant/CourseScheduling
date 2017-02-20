# Course Scheduling

## Initial Plan
In my initial plan, I illustrated my main idea of the course scheduling project,
described the Coffman-graham algorithm that I will be working on, and some difficulties as well as interesting points.
[research-initial-plan.pdf](research-initial-plan.pdf)

## TODOs
1. Allow input courses already taken and schedule at the middle.
2. Evaulate the quality of solution
3. Compare it with other job scheduling algorithms

## Current Course Scheduling Algorithm
### Algorithm Explanations
#### in main:
```
Load specialization info into SpecsTable
load course infomation into graphs
For each course in graph:
    update the course dependent info
    update course specialization satisfaction info
Start to do multigraph scheduling
```


#### in Scheduling algorithm

- L: is the scheduling output, which is initially ```[[]]``` before doing
scheduling for all the graphs.

- Q: store the courses that are going to be scheduled into L. prereqs of all courses in the queue are already satisfied.

- define number of courses in graph to be n.

- define the number of levels in L to be m. 0<m<n

- define the maximum width of a level to be w.  0<w<n and w = n/m

```
INPUT:
    - L: current schedule
    - graph: a course graph
    - specsTable: store specs that should be satisfied
    - upperBound: above what levels a upper standing course can be assgined

OUTPUT: L

initialize Q, maxheap structure, and add courses without prereqs into it

while Q is not empty:                                                           # O(n) times
    currentCourse = Q.pop()         # O(1)

    discard currentCourse if it does not satisfy any specializations

    if the highest level has dependents, it has to be assigned to a new level.
        Then assigned = True
    else: assigned = False

    if not assigned:       # the highest level does not have cur's dependents
        step = the second highest level index
        if the highest level is full, we have to create a new level
            and then create more levels until it find the nearest quarter that
            this course is offered.                                             # O(w)
        lastStep = the highest level index (lowest acceptable one so far)

        while not assigned to the schedule and step >= 0: # O(m) times

            if there are dependents in level L[step]:           # O(w)
                it cannot be assigned to a higher level,
                 we assign it to the level L[lastStep]
                 assigned = True

            else:
                if course is upper standing only and step < upperBound:
                    assign it to the level L[lastStep]
                    assigned = True

                else if this level is not full,
                    and currentCourse will be offered this quarter,
                    then this is a possible level for this course.  # O(w)
                    we will mark:
                        lastStep = step
            step--

        if the course is still not assigned after looking over all levels in schedule:
            course will be assigned to the lowest acceptable level L[lastStep]

        we are sure that the course is assigned, then we will add those courses
            that will be satisfied after assigning this course into Q           # O(nlogn)

        add currentCourse units into the total units assigned       # O(1)

    clear empty levels at the end of L
    return L
```

- creating new levels until find the nearest quarter that this course is offered is
O(1) because it will create at most 3 levels for a course
- any pop or push operation is O(1)
- the first while loop will loop through O(n) times
- between first while loop and the third one: O(n+2w) = O(n+w)=O(n)
- third while loop: O(m) times
- in third while loop: O(2w) = O(w)
- lastly, push at most n elements into a max heap is O(nlogn)
- total is O(n)\*(O(n)+O(m)\*O(w) + O(nlogn)) = O(n)\*O(nlogn) = O(n^2logn)



## Current Results
1. Max heap with a heuristic estimation for course values for better performance, but increase the time complexity

2. It will make schedules on a upper bound range and pick the most efficient one.

3. solve the problem that some courses are upper standing student only.
    Set a upper bound advanced. The bound will prevent the algorithm from assigning upper standing only courses into a level < upper bound (specified in function).

4. it can pick more courses randomly to fullfill the 11 upper requirement after loading 11 upper requirement in the specialization txt file.

5. A Simple Schedule

    This schedule can handle the following conditions:

    1. GE requirement
    2. specialization requirement
    3. the quarter offering and course units
    4. Some courses are upper division standing only

    **sample:**
    ```
    CS Student specialized in Intelligent System.
    Take 17 credits per quarter:
    year 1 quarter 1: ['I&CSCI6B', 'I&CSCI31', 'MATH2A', 'GEII-1', 'I&CSCI90']
    year 1 quarter 2: ['I&CSCI6D', 'I&CSCI51', 'MATH2B']
    year 1 quarter 3: ['MATH3A', 'STATS67', 'I&CSCI32', 'GEII-2']
    year 2 quarter 1: ['COMPSCI132', 'IN4MATX131', 'I&CSCI33', 'IN4MATX43']
    year 2 quarter 2: ['COMPSCI178', 'I&CSCI45C', 'COMPSCI122A', 'COMPSCI133']
    year 2 quarter 3: ['I&CSCI46', 'COMPSCI177', 'I&CSCI53+53L']
    year 3 quarter 1: ['COMPSCI161', 'COMPSCI143A', 'COMPSCI171', 'COMPSCI112']
    year 3 quarter 2: ['COMPSCI116', 'COMPSCI162', 'COMPSCI175', 'COMPSCI167']
    year 3 quarter 3: ['COMPSCI163', 'GEIV-1', 'GEIV-2', 'GEIV-3']
    year 4 quarter 1: ['COMPSCI151', 'IN4MATX121', 'COMPSCI169', 'GEVI-1']
    year 4 quarter 2: ['COMPSCI152', 'GEVII-1', 'GEVIII-1']
    best upper bound: year 2 quarter 3
    ```

6. Original coffman-graham algorithm.
    - [directedGraphRepresentation](coffman_graham_algorithm/directedGraphRepresentation.py)
    - [coffman-graham algorithm](coffman_graham_algorithm/coffman-grapham.py)

7. Crawler
    - [WebSoc and prerequistes Crawler (using beautiful soup and requests libraries)](WebSoc.py)

    - Right now it still cannot get those courses without prereqs automatically
    - For courses such as I&CSCI 51, have to manually modify it to be I&CSCI 51+51L, and change the units to be 6.

8. Courses information I got from [www.reg.uci.edu](https://www.reg.uci.edu/cob/prrqcgi?term=201703&dept=COMPSCI&action=view_by_term#115) and [WebSoc](https://www.reg.uci.edu/perl/WebSoc). I integrated my crawlers into one on week 4 in Winter quarter.

    **sample**:
    - [Courses info in some departments](info/test/fullcourses.txt)

    In the txt file, each line contains info of a course and the line is separated by ";". Line is in the following format:
    ```[department code];[course num];[title];[prereqs];[units];[quarters];[isUpperOnly]```
    e.g.
    ```I&CSCI;6D;DISCRET MATH FOR CS;[{'I&CSCI6B'}];4;{0, 1, 2};False```


    NOTE: Courses information here is just used for testing and is not accurate because the quarters a course will be offered may vary each year.


9. CS specializations information I got manually from [catalogue.uci.edu](http://catalogue.uci.edu/donaldbrenschoolofinformationandcomputersciences/departmentofcomputerscience/#majorstext)

    **sample**:
    - [CS specializations](info/test/specializations.txt)




## Research Project Schedule

### 2017 Winter Quarter
During winter quarter, I will implement the algorithm and resolve dificulties described. I
will also have a working application done by the end of this quarter.
- **Week 1:** (Done) Find a method to represent the study plan graph.

- **Week 2:** (Done) Apply the basic Coffman-Graham algorithm, which defines a fixed width bound $ W $, and test its performance in this particular course scheduling problem assuming that the number of classes a student takes will not exceed a fixed width bound.

- **week 3:** (Done) Collect courses information online by using web crawlers.

- **Week 4, 5, 6:** (In progress) Modify the algorithm to solve difficulties illustrated and test the quality of the final algorithm.

- **week 7, 8, 9, 10:** Find other similar algorithms and compare them with coffman-graham algorithm. 

### 2017 Spring Quarter

During spring quarter, I will focus on writing and revising the project report. 

- **Week 1:** An outline of the project report.

- **Week 2:** First 1/3 of the project report.

- **Week 3:** Second 1/3 of the project report.

- **Week 4:** Third 1/3 of the project report.

- **Week 5, 6:** Second draft of the project report.

- **Week 7, 8:** Third draft of the project report.

- **Week 9:**  Forth draft of the project report. 

- **Week 10:** Final draft of the project report. 