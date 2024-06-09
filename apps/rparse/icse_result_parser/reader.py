from .student import Student

def clean_line(line):
    return list(filter(lambda x: x != "", map(lambda x: x.strip(), line.split(" "))))


POSSIBLE_RESULTS = ["PCA", "PCNA", "SPC", "SPCNA", "ABS"]

class ResultReader(object):
    """
    Dumb Reader Class to support reading from a file of specific format
    Can be extended to multiple classes later
    """

    def __init__(self):
        self._major_subjects = set()
        self._component_subjects = {}
        
    """
    Data format
        UNIQUE ID
        NAME
        D.O.B.
        GENDER
        TOE
        NTY SCD
        RESULT
    1     ddddddd                   -> unique id
    2     XXXXX XXXX                -> name
    3     DD/MM/YYYY                -> dob (discard)
    4     BOY/GIRL                  -> gender
    5     1                         -> toe (discard)
    6     I                         -> nty (discard)
    7     3                         -> scd (discard)
    8     SRL No XXXXX              -> scd (discard)
    9     XXXXX/ XXX                -> unique id 2 
    10    Son of mother's name and father's name -> parents (discard)
    11    PCA                       -> result
    12    ENG - 1 - DD (EN1-DD,EN2-DD) HIN - 1 - DD HCG - 2 - DD (HCS-DD,GEO-DD) MAT - 1 - DD SCI - 1 - DD -> mark line 1
    13    (PHY-DD,CHE-DD,BIO-DD) PED - 1 - DD SUPW:A -> mark line 2

    Mark line could also be a single line if a student is absent

    Someday I'll write tests and this comment will be shorter
    """
    def read_page(self, page):
        students = []
        lines = page.split("\n")
        
        # Skip header lines and chunk the data
        num_header_lines = 7
        chunk = [] 
        marks_read = False
        result_read = False

        for line_idx in range(num_header_lines, len(lines)):
            line = lines[line_idx]   
            chunk.append(line)
            if "SUPW" in line:
                marks_read = True
            if line in POSSIBLE_RESULTS:
                result_read = True
            
            if marks_read and result_read:
                student = self._get_student_result_from_chunk(chunk)    
                students.append(student)
                
                # Reset chunk
                chunk = []
                marks_read = False
                result_read = False
        
        return students

    def _get_student_result_from_chunk(self, chunk):
        unique_id_1 = chunk[0]
        name = chunk[1]
        gender = chunk[3]
        
        # For absent student lines with SRL No are not present
        was_absent = "ABS" in chunk
        unique_id_2 = chunk[8] if not was_absent else chunk[7]
        mark_line = ""
        result = None

        # Ordering of mark line and result is non-deterministic
        # For students with ABS results result appears after the marks line whereas
        # it is opposite for other students
        start_idx = 10 if not was_absent else 9

        for line in chunk[start_idx:]:
            if line in POSSIBLE_RESULTS:
                result = line
            else:
                mark_line += line + " "

        return Student(unique_id_1, unique_id_2, name, gender, result, self._read_subjects(mark_line))
        
    def _read_subjects(self, mark_line):
        subjects = {}
        cur_subject = None

        """
        mark_line is of the form 
            for present results
                ENG - 1 - 93 (EN1-94,EN2-92) HIN - 1 - 91 HCG - 2 - 89 (HCS-94,GEO-83) MAT - 1 - 91 SCI - 1 - 91 (PHY-94,CHE-92,BIO-86) PED - 1 - 92 SUPW:A 
            for absent students
                ENG - X -XXX PUN - X -XXX HCG - X -XXX MAT - X -XXX SCI - X -XXX CTA - X -XXX SUPW:X

        subj_reading_type tracks the parsing stage of ENG - 1 - 93 data
        0 indicates subj_code is to be read
        1 indicates subj_grade is to be read
        2 indicates subj_marks are to be read
        3 indicates everything is read
        """
        subj_reading_type = 0

        for subj_data in mark_line.split(" "):
            # eg SUPW:A
            if ":" in subj_data:
                subj_code, grade = subj_data.split(":")
                subjects[subj_code] = grade

            # eg (EN1-94,EN2-92)
            elif subj_data.startswith("("):
                component_dict = {}
                # Remove opening and closing braces
                for component_subject_data in subj_data[1:-1].split(","):
                    subj_code, marks = component_subject_data.split("-")
                    component_dict[subj_code] = marks            
                    
                subjects[cur_subject]["components"] = component_dict
                self._component_subjects[cur_subject] = component_dict.keys()

            elif subj_data == "-" or len(subj_data) == 0:
                continue

            else:
                subj_data = subj_data.replace("-", "")
                if subj_reading_type == 0:
                    cur_subject = subj_data
                    self._major_subjects.add(cur_subject)
                elif subj_reading_type == 1:
                    subjects[cur_subject] = {"grade": subj_data}
                else:
                    subjects[cur_subject]["marks"] = subj_data

                subj_reading_type = (subj_reading_type + 1) % 3
        return subjects
  
    def get_major_subjects(self):
        return self._major_subjects
    
    
    def get_component_subjects(self):
        return self._component_subjects

