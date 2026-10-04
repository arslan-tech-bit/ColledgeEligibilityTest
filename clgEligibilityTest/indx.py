
from functools import reduce

subjects = {"Math", "Physics", "Chemistry", "English", "Math"}
course_codes = frozenset({"CS101", "EE102", "ME103"})

students = []
marks = {}

n = int(input("How many students: "))

for i in range(n):
    name = input("Enter name: ")
    roll = int(input("Enter roll no: "))

    m = []
    for sub in subjects:
        x = int(input("Enter marks in " + sub + ": "))
        m.append(x)

    students.append((name, roll))
    marks[roll] = m


def logger(f):
    def inner(s, m):
        print("Checking", s[0])
        ans = f(s, m)

        if ans is None:
            print("Check failed for", s[0])
        else:
            print("Done", s[0], "-> eligible:", ans[3])

        return ans

    return inner


def check_details(f):
    def inner(s, m):
        if len(s) != 2:
            print("bad student details")
            return None

        return f(s, m)

    return inner


def check_marks(f):
    def inner(s, m):
        for x in m:
            if x < 0 or x > 100:
                print("bad marks")
                return None

        return f(s, m)

    return inner


def bonus(m):
    if len(m) == 0:
        return 0

    if m[0] >= 90:
        return 2 + bonus(m[1:])

    return bonus(m[1:])


@logger
@check_details
@check_marks
def eligibility(s, m):
    per = sum(m) / len(m)

    if per >= 60 and min(m) >= 40:
        ok = True
    else:
        ok = False

    return (s[0], s[1], per, ok)


check = eligibility

results = list(map(lambda s: check(s, marks[s[1]]), students))

results = list(filter(lambda r: r is not None, results))

eligible = list(filter(lambda r: r[3], results))
not_eligible = list(filter(lambda r: not r[3], results))


def get_courses(per):
    if per > 90:
        return ["Robotics", "AI & DS", "AI/ML", "Mechanical",
                "Civil", "CS (Core)", "Cyber Security"]

    elif per > 80:
        return ["AI/ML", "AI & DS", "Civil", "Mechanical",
                "CS (Core)", "Cyber Security"]

    elif per > 70:
        return ["Civil", "Mechanical"]

    elif per > 60:
        return ["Mechanical"]

    else:
        return []


print("\nCourses offered:", ", ".join(sorted(course_codes)))

if len(eligible) == 0:
    print("\nThere are no eligible students for college")

elif len(not_eligible) == 0:
    print("\nAll students are eligible")

    for r in eligible:
        print(r[0], r[2])

else:
    print("\nEligible:")

    for r in eligible:
        print(r[0], r[2])

    print("\nNot eligible:")

    for r in not_eligible:
        print(r[0], r[2])


if results:
    avg = reduce(lambda a, b: a + b[2], results, 0) / len(results)

    top = reduce(
        lambda a, b: a if a[2] > b[2] else b,
        results
    )

    print("\nAverage:", avg)
    print("Topper:", top[0], top[2])


ranked = sorted(eligible, key=lambda r: r[2], reverse=True)

rank_of = {}

for i in range(len(ranked)):
    rank_of[ranked[i][1]] = i + 1


if ranked:
    print("\n" + "=" * 40)
    print("TOP 3 ELIGIBLE STUDENTS")
    print("=" * 40)

    print(f"{'Rank':<8}{'Name':<14}{'Percentage'}")

    for r in ranked[:3]:
        print(f"{rank_of[r[1]]:<8}{r[0]:<14}{r[2]:.2f}")


print("\n" + "=" * 82)
print("FULL LIST")
print("=" * 82)

print(
    f"{'S.No.':<8}"
    f"{'Name':<16}"
    f"{'Total Marks':<14}"
    f"{'Percentage':<14}"
    f"{'Eligibility':<16}"
    f"{'Courses'}"
)

print("=" * 82)

sno = 1

for r in results:
    total = sum(marks[r[1]])

    if r[3]:
        status = "Eligible"
        courses = get_courses(r[2])

        if courses:
            if len(courses) == 1:
                count = "1 course"
            else:
                count = str(len(courses)) + " courses"
        else:
            count = "None"

    else:
        status = "Not Eligible"
        count = "-"

    print(
        f"{str(sno) + '.':<8}"
        f"{r[0]:<16}"
        f"{total:<14}"
        f"{str(round(r[2], 2)) + '%':<14}"
        f"{status:<16}"
        f"{count}"
    )

    sno += 1


print("=" * 82)
print("\nSTUDENT WISE ELIGIBLE COURSES")
print("=" * 82)

for r in eligible:
    print(f"\n{r[0]} ({round(r[2], 2)}%)")
    print("Eligible for :-")

    courses = get_courses(r[2])

    if courses:
        for i in range(len(courses)):
            print(f"        {i + 1}. {courses[i]}")
    else:
        print("        No course available for this percentage")
