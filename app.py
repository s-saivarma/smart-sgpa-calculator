from flask import Flask, request, render_template_string
import json

app = Flask(__name__)

semester_data = {
    "1-1": {
        "subjects": ["Mathematics-I", "Applied Physics", "Basic Electrical Engineering", "Engineering Chemistry", "Programming for Problem Solving"],
        "labs": ["Physics Lab", "Chemistry Lab", "Programming Lab"]
    },
    "1-2": {
        "subjects": ["Mathematics-II", "English", "Basic Electronics", "Engineering Mechanics", "Environmental Science"],
        "labs": ["English Lab", "Basic Electronics Lab", "Workshop Lab"]
    },
    "2-1": {
        "subjects": ["Network Theory", "Electronic Devices and Circuits", "Signals and Systems", "Digital Logic Design", "Probability Theory"],
        "labs": ["Electronic Devices Lab", "Digital Logic Lab", "Network Lab"]
    },
    "2-2": {
        "subjects": ["Analog Communications", "Pulse and Digital Circuits", "Electromagnetic Waves", "Control Systems", "Object Oriented Programming"],
        "labs": ["Pulse Circuits Lab", "OOP Lab", "Communication Lab"]
    },
    "3-1": {
        "subjects": ["Microprocessors", "Linear IC Applications", "Digital Communications", "Antenna Theory", "Managerial Economics"],
        "labs": ["Microprocessors Lab", "LIC Lab", "Digital Communication Lab"]
    },
    "3-2": {
        "subjects": ["VLSI Design", "Digital Signal Processing", "Microwave Engineering", "Embedded Systems", "Computer Networks"],
        "labs": ["VLSI Lab", "DSP Lab", "Embedded Systems Lab"]
    },
    "4-1": {
        "subjects": ["Wireless Communication", "Optical Communication", "Satellite Communication", "Internet of Things", "Professional Elective-I"],
        "labs": ["Wireless Lab", "Optical Lab", "IoT Lab"]
    },
    "4-2": {
        "subjects": ["Machine Learning", "Radar Systems", "5G Communication", "Professional Elective-II", "Project Work"],
        "labs": ["ML Lab", "Simulation Lab", "Project Lab"]
    }
}

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Smart SGPA Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f7fb;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 850px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 0 10px rgba(0,0,0,0.15);
        }
        h1, h2 {
            text-align: center;
        }
        label {
            font-weight: bold;
            display: block;
            margin-top: 10px;
        }
        input, select {
            width: 100%;
            padding: 10px;
            margin-top: 5px;
            border-radius: 8px;
            border: 1px solid #ccc;
            box-sizing: border-box;
        }
        .box {
            background: #f9fbff;
            border: 1px solid #d9e6f5;
            border-radius: 10px;
            padding: 12px;
            margin-top: 12px;
        }
        button {
            width: 100%;
            margin-top: 20px;
            padding: 12px;
            border: none;
            border-radius: 10px;
            background: #2563eb;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background: #1d4ed8;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background: #ecfdf5;
            border-left: 6px solid #10b981;
            border-radius: 10px;
            font-weight: bold;
        }
        .failed-result {
            margin-top: 20px;
            padding: 15px;
            background: #fef2f2;
            border-left: 6px solid #dc2626;
            border-radius: 10px;
            font-weight: bold;
            color: #b91c1c;
        }
        table {
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid #ccc;
        }
        th, td {
            padding: 10px;
            text-align: center;
        }
        th {
            background: #eef4ff;
        }
        .fail-row {
            background-color: #fee2e2;
            color: #b91c1c;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Smart SGPA Calculator</h1>

        <form method="post" action="/calculate">
            <label>Student Name</label>
            <input type="text" name="name" required>

            <label>College Email ID</label>
            <input type="email" name="email" required>

            <label>Year</label>
            <select name="year" id="year" onchange="loadSubjects()" required>
                <option value="">Select Year</option>
                <option value="1">1st Year</option>
                <option value="2">2nd Year</option>
                <option value="3">3rd Year</option>
                <option value="4">4th Year</option>
            </select>

            <label>Semester</label>
            <select name="sem" id="sem" onchange="loadSubjects()" required>
                <option value="">Select Semester</option>
                <option value="1">Sem 1</option>
                <option value="2">Sem 2</option>
            </select>

            <div id="subjectsContainer"></div>

            <button type="submit">Calculate SGPA</button>
        </form>

        {% if failed %}
        <div class="failed-result">{{ result }}</div>
        {% elif result %}
        <div class="result">{{ result }}</div>
        {% endif %}

        {% if entered_marks %}
        <h2>Entered Marks</h2>
        <table>
            <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Marks</th>
                <th>Grade Point</th>
                <th>Credit</th>
            </tr>
            {% for item in entered_marks %}
            <tr class="{% if item.is_failed %}fail-row{% endif %}">
                <td>{{ item.name }}</td>
                <td>{{ item.type }}</td>
                <td>{{ item.marks }}</td>
                <td>{{ item.grade_point }}</td>
                <td>{{ item.credit }}</td>
            </tr>
            {% endfor %}
        </table>
        {% endif %}
    </div>

    <script>
        const semesterData = {{ semester_data | safe }};

        function loadSubjects() {
            const year = document.getElementById("year").value;
            const sem = document.getElementById("sem").value;
            const key = `${year}-${sem}`;
            const container = document.getElementById("subjectsContainer");

            container.innerHTML = "";

            if (!semesterData[key]) {
                return;
            }

            const subjects = semesterData[key].subjects;
            const labs = semesterData[key].labs;

            const h1 = document.createElement("h2");
            h1.innerText = "Subjects";
            container.appendChild(h1);

            subjects.forEach(subject => {
                const div = document.createElement("div");
                div.className = "box";
                div.innerHTML = `
                    <label>${subject}</label>
                    <input type="number" name="${subject}" min="0" max="100" required placeholder="Enter marks">
                `;
                container.appendChild(div);
            });

            const h2 = document.createElement("h2");
            h2.innerText = "Labs";
            container.appendChild(h2);

            labs.forEach(lab => {
                const div = document.createElement("div");
                div.className = "box";
                div.innerHTML = `
                    <label>${lab}</label>
                    <input type="number" name="${lab}" min="0" max="100" required placeholder="Enter marks">
                `;
                container.appendChild(div);
            });
        }
    </script>
</body>
</html>
"""

PASS_MARK = 24
SUBJECT_CREDIT = 3
LAB_CREDIT = 1

def marks_to_grade_point(marks):
    if marks >= 90:
        return 10
    elif marks >= 80:
        return 9
    elif marks >= 70:
        return 8
    elif marks >= 60:
        return 7
    elif marks >= 50:
        return 6
    elif marks >= 40:
        return 5
    elif marks >= PASS_MARK:
        return 4
    else:
        return 0

@app.route("/")
def home():
    return render_template_string(HTML_PAGE, semester_data=json.dumps(semester_data))

@app.route("/calculate", methods=["POST"])
def calculate():
    name = request.form["name"]
    email = request.form["email"]
    year = request.form["year"]
    sem = request.form["sem"]

    key = f"{year}-{sem}"
    sem_info = semester_data.get(key)

    if not sem_info:
        return render_template_string(
            HTML_PAGE,
            semester_data=json.dumps(semester_data),
            result="Invalid year/semester selected."
        )

    total_credit_points = 0
    total_credits = 0
    entered_marks = []
    has_failed = False

    for subject in sem_info["subjects"]:
        mark = int(request.form.get(subject, 0))

        if mark < PASS_MARK:
            has_failed = True
            entered_marks.append({
                "name": subject,
                "type": "Subject",
                "marks": "F",
                "grade_point": "F",
                "credit": "F",
                "is_failed": True
            })
        else:
            gp = marks_to_grade_point(mark)
            total_credit_points += gp * SUBJECT_CREDIT
            total_credits += SUBJECT_CREDIT
            entered_marks.append({
                "name": subject,
                "type": "Subject",
                "marks": mark,
                "grade_point": gp,
                "credit": SUBJECT_CREDIT,
                "is_failed": False
            })

    for lab in sem_info["labs"]:
        mark = int(request.form.get(lab, 0))

        if mark < PASS_MARK:
            has_failed = True
            entered_marks.append({
                "name": lab,
                "type": "Lab",
                "marks": "F",
                "grade_point": "F",
                "credit": "F",
                "is_failed": True
            })
        else:
            gp = marks_to_grade_point(mark)
            total_credit_points += gp * LAB_CREDIT
            total_credits += LAB_CREDIT
            entered_marks.append({
                "name": lab,
                "type": "Lab",
                "marks": mark,
                "grade_point": gp,
                "credit": LAB_CREDIT,
                "is_failed": False
            })

    if has_failed:
        result = f"{name} ({email}) - Year {year} Sem {sem} : Failed"
        return render_template_string(
            HTML_PAGE,
            semester_data=json.dumps(semester_data),
            result=result,
            entered_marks=entered_marks,
            failed=True
        )

    sgpa = round(total_credit_points / total_credits, 2) if total_credits else 0

    return render_template_string(
        HTML_PAGE,
        semester_data=json.dumps(semester_data),
        result=f"{name} ({email}) - Year {year} Sem {sem} SGPA: {sgpa}",
        entered_marks=entered_marks,
        failed=False
    )

if __name__ == "__main__":
    app.run()