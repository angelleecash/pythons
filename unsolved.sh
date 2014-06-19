mysql -uchenliang -pzxcvb -B --skip-column-names -e "use private_2;select subTasks from mission where id=5" | sed -e "s/\\\\n//g" > mission_data

python parse_json.py mission_data > task_knowledge

mysql -uchenliang -pzxcvb -B --skip-column-names -e "use private_2;select * from submission" > submission

mysql -uchenliang -pzxcvb -B --skip-column-names -e "use common;select * from knowledge" > knowledges 


mysql -uchenliang -pzxcvb -B --skip-column-names -e "use private_2;select * from student" > students
mysql -uchenliang -pzxcvb -B --skip-column-names -e "use private_2;select id,assignmentId from study_task" > study_tasks
mysql -uchenliang -pzxcvb -B --skip-column-names -e "use private_2;select studentId,questionId,correctness from submission_review" > submission_review
mysql -uchenliang -pzxcvb -B --skip-column-names -e "use private_2;select id,questionIds from assignment" > assignments

cat assignments | sed "s/     / /g" | tr -d "[]" | sed -e "s/,/ /g" > assignmentsToQuestionIds

awk -F " " -f unsolved.awk assignmentsToQuestionIds submission_review study_tasks knowledges task_knowledge students submission groups > "不会做统计"

