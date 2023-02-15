# librairies importation
import tkinter as TK
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import datetime as dt


class Laboratory():
    def __init__(self, name):
        self._Name = str(name)
        self._Head = None
    def _get_Name(self):
        return self._Name
    def _get_Head(self):
        return self._Head
    def _set_Head(self, newHead):
        if isinstance(newHead, Internal):
            self._Head = newHead
    Name = property(_get_Name)
    Head = property(_get_Head)
    def __repr__(self):
        return self._Name


class Staff():
    def __init__(self, lenom, leprenom, legenre, ladate, lepays):
        self.__Name = str(lenom)
        self.__FirstName = str(leprenom)
        self.__Gender = str(legenre)
        self.__BD = ladate
        if self.__BD == None:
            self.__BD = dt.date(1900,1,1)
        else :
            self.__BD = dt.date(int(ladate[:4]),int(ladate[5:7]), int(ladate[8:]))
        self.__Country = str(lepays)
        self._Bibliography = []
        self._Projects = []
        self._PhD = []
    def _get_Name(self):
        return self.__Name
    def _get_FirstName(self):
        return self.__FirstName
    def _get_Gender(self):
        return self.__Gender
    def _get_BD(self):
        return self.__BD
    def _get_Country(self):
        return self.__Country
    def _get_Bibliography(self):
        return self._Bibliography
    def _get_Projects(self):
        return self._Projects
    def _get_PhD(self):
        return self._PhD
    Name = property(_get_Name)
    FirstName = property(_get_FirstName)
    Gender = property(_get_Gender)
    BD = property(_get_BD)
    Country = property(_get_Country)
    Bibliography = property(_get_Bibliography)
    Projects = property(_get_Projects)
    PhD = property(_get_PhD)
    def release(self,publication):
        if isinstance(publication, (Publication, Articles, Journal, Conference, Report)):
            self._Bibliography.append(publication)
            if self not in publication.Authors:
                publication.add_Author(self)
    def add_Project(self, project):
        if isinstance(project, (Research_Project)) :
            self._Projects.append(project)
            if self not in project.Members :
                project._Members.append(self)
    def add_PhD(self, phd):
        if isinstance(phd, PhD) :
            self._PhD.append(phd)
    def __repr__(self):
        if self.__Gender == 'M' :
            return "M. {} {}".format(self.__Name, self.__FirstName)
        elif self.__Gender == 'F':
            return "Mme. {} {}".format(self.__Name, self.__FirstName)
        else :
            return "{} {}".format(self.__Name, self.__FirstName)
        
        
class Internal(Staff):
    def __init__(self, lenom, leprenom, legenre, ladate, lepays,lebureau):
        super().__init__(lenom, leprenom, legenre, ladate, lepays)
        self._Career = list()
        self._TauxAppartenance = {}
        self._Office = str(lebureau)
    def _get_Office(self):
        return self._Office
    def _set_Office(self, newOffice):
        self._Office = str(newOffice)
    Office = property(_get_Office)
    def _get_Career(self):
        return self._Career
    def _get_TauxAppartenance(self):
        return self._TauxAppartenance
    def _add_Position(self, newPosition, debut, fin) :
        self._Career.append([str(newPosition), str(debut), str(fin)])
    def _set_TauxAppartenance(self, axe_recherche, sontaux):
        if isinstance(axe_recherche, Axe_Recherche) :
            self._TauxAppartenance[axe_recherche] = float(sontaux)
            axe_recherche._TauxAppartenance[self] = float(sontaux)
    Taux = property(_get_TauxAppartenance)
    Career = property(_get_Career)
    



#Internal_1 = Internal("Kang", "Laetitia", "F", "1999/09/22", "Cambodge", "A")
#Internal_2 = Internal("Zhang", "Alex", "M", "1999/07/25", "Chine", "A")
#Internal_3 = Internal("Pho", "Anh-Minh", "M", "2000/04/02", "Chine", "A")
#Article_1 = Articles("Titre", "2020/02/15", "http:")
#Journal_1 = Journal("2020/02/15", "Titre", "http:", "Nom", 25, "Q3")
#Internal_1._set_Bureau("B")
#Internal_1._add_Position("Masterant", "03/09/2006", "04/07/2008")
#Internal_1._add_Position("Doctorant", "04/09/2008", "04/07/2009")
#print(Internal_1.Bibliography)

 
#Laboratoire = Laboratory("coucou")
#Laboratoire._set_Head(Internal_1)
#print(Laboratoire.Head)
        
class External(Staff):
    def __init__(self, lenom, leprenom, legenre, ladate, lepays, letablissement):
        super().__init__(lenom, leprenom, legenre, ladate, lepays)
        self._Poste = None
        self._Laboratoire = None
        self._Company = str(letablissement)
        self._History = list()
    def _get_Poste(self):
        return self._Poste
    def _get_Laboratoire(self):
        return self._Laboratoire
    def _get_Company(self):
        return self._Company
    def _get_History(self):
        return self._History
    def _set_Poste(self, newPoste):
        self._Poste = str(newPoste)
    def _set_Labo(self, newLabo):
        self._Laboratoire = str(newLabo)
    def _set_Company(self, newCompany):
        self._Company = str(newCompany)
    def _AddInvitation(self, debut, fin, inviteur):
        self._History.append([str(debut),str(fin), str(inviteur)])
    Poste = property(_get_Poste)
    Laboratoire = property(_get_Laboratoire)
    Company = property(_get_Company)
    History = property(_get_History)

class Axe_Recherche():
    def __init__(self, lenom):
        self.__Name = str(lenom)
        self._TauxAppartenance = {}
        self._Head = {}
    def _get_Name(self):
        return self.__Name
    def _get_Head(self):
        return self._Head
    def _get_TauxAppartenance(self):
        return self._TauxAppartenance
    def _set_Head(self,newHead, letaux):
        if isinstance(newHead, Internal):
            self._Head[newHead] = letaux
            self._TauxAppartenance[newHead] = letaux
            if newHead not in self._TauxAppartenance:
                newHead._TauxAppartenance[self] = letaux
    Head = property(_get_Head)
    Name = property(_get_Name)
    TauxAppartenance = property(_get_TauxAppartenance)
    def _set_TauxAppartenance(self,internal,sontaux):
        #assert sontaux>=0 and sontaux<=1
        if isinstance(internal, Internal) and internal not in self._TauxAppartenance:
            self._TauxAppartenance[internal] = sontaux
            internal._TauxAppartenance[self] = sontaux
    def __repr__(self):
        return "{}".format(self.__Name)

    
class Publication():
    pass
    
    
class Articles(Publication):
    def __init__(self, letitre, ladate, leDOI):
        self._Title = str(letitre)
        self._Available = dt.date(int(ladate[:4]),int(ladate[5:7]), int(ladate[8:]))
        self._Authors = []
        self._DOI = str(leDOI)
        self._Provenance = None
    def _get_Authors(self):
        return self._Authors
    def _get_Available(self):
        return self._Available
    def _get_Title(self):
        return self._Title
    def _get_DOI(self):
        return self._DOI
    def _get_Provenance(self):
        return self._Provenance
    def add_Author(self, author):
        if isinstance(author, (Staff, Internal, External)):
            self._Authors.append(author)
            if self not in author.Bibliography :
                author.release(self)
    Authors = property(_get_Authors)
    Available = property(_get_Available)
    Title = property(_get_Title)
    DOI = property(_get_DOI)
    def __repr__(self):
        return "{} ({})".format(self._Title, self._Available.year)
        
#Article_1 = Articles([Internal_1, Internal_2], "22/09/2020", "Article 1", "http//:jspquoi.com", "Laboratoire")

class Journal(Articles):
    def __init__(self, letitre, ladate,leDOI, larevue):
        super().__init__(letitre, ladate, leDOI)
        self._Mag = str(larevue)
        if isinstance(self._Mag, Magazine) and self not in self._Mag.Publications:
            self._Mag.Publications.append(self)
    def _get_Mag(self):
        return self._Mag
    """def _set_revue(self, newRevue):
        for revue in Interface().Laboratory["Magazines"]:
            if revue.Name == newRevue or revue.Short == newRevue:
                self._Mag = revue"""
    Mag = property(_get_Mag)
    
   
#LaRevue = Magazine("LeMonde", "LM")     
#LeA = Journal("Titre", "2021/03/12", "http://", LaRevue)

class Magazine():
    def __init__(self, lenom, lacronyme):
        self._Name = str(lenom)
        self._Short = str(lacronyme)
        self._IF = {}
        self._Quartile = {}
        self._Publications = []
    def _get_Name(self):
        return self._Name
    def _get_Short(self):
        return self._Short
    def _get_IF(self):
        return self._IF
    def _get_Quartile(self):
        return self._Quartile
    def _get_Publications(self):
        return self._Publications
    Name = property(_get_Name)
    Short = property(_get_Short)
    IF = property(_get_IF)
    Quartile = property(_get_Quartile)
    Publications = property(_get_Publications)
    def _add_IF(self, year, value):
        if isinstance(year, str):
            self._IF[year] = float(value)
    def _add_Quartile(self, year, value):
        if isinstance(year, str):
            self._Quartile[year] = value
    def _add_Publications(self, journal):
        if isinstance(journal, Journal):
            self._Publications.append(journal)
    def __repr__(self):
        return "{} ({})".format(self.Name, self.Short)
    
class Conference(Articles):
    def __init__(self, letitre, ladate, leDOI, lenom, lesdates, lelieu):
        super().__init__(letitre, ladate, leDOI)
        self._Name = str(lenom)
        self._Dates = str(lesdates)
        self._Place = str(lelieu)
    def _get_Name(self):
        return self._Name
    def _get_Dates(self):
        return self._Dates
    def _get_Place(self):
        return self._Place
    Name = property(_get_Name)
    Dates = property(_get_Dates)
    Place = property(_get_Place)

class Report(Publication):
    def __init__(self, letitre, ladate):
        self._Title = str(letitre)
        self._Available = dt.date(int(ladate[:4]),int(ladate[5:7]), int(ladate[8:]))
        self._Authors = []
    def _get_Title(self):
        return self._Title
    def _get_Available(self):
        return self._Available
    def _get_Authors(self):
        return self._Authors
    def add_Author(self, author):
        if isinstance(author, (Staff, Internal, External)):
            self._Authors.append(author)
            if self not in author.Bibliography:
                author.release(self)
    Title = property(_get_Title)
    Available = property(_get_Available)
    Authors = property(_get_Authors)
    def __repr__(self):
        return "{} ({})".format(self.Title, self.Available.year)

class Project():
    def __init__(self, lenom):
        self._Name = str(lenom)
        self._ProdRef = None
    def _get_ProdRef(self):
        return self._ProdRef    
    def _set_ProdRef(self, publication, J, C, R):
        for proj in J:
            if proj.Title == publication or proj.DOI == publication:
                self._ProdRef = proj
                #break
        for proj in C:
            if proj.Title == publication or proj.DOI == publication:
                self._ProdRef = proj
                #break
        for proj in R:
            if proj.Title == publication :
                self._ProdRef = proj
                #break
    ProdRef = property(_get_ProdRef)

class Research_Project(Project):
    def __init__(self, lenom, ladatefinprev, ladatedebut, lacronyme=""):
        super().__init__(lenom)
        self._Start = ladatedebut
        if self._Start == None:
            self._Start == dt.date(1900,1,1)
        else :
            self._Start = dt.date(int(ladatedebut[:4]),int(ladatedebut[5:7]), int(ladatedebut[8:]))
        self._ExpectedEnd = dt.date(int(ladatefinprev[:4]),int(ladatefinprev[5:7]), int(ladatefinprev[8:]))
        self._End = None
        self._Budget = None
        self._Short = str(lacronyme)
        self._Members = []
        self._Head = None
        self._CompaniesInvolved = {}
    def _get_Name(self):
        return self._Name
    def _get_Start(self):
        return self._Start
    def _get_ExpectedEnd(self):
        return self._ExpectedEnd
    def _get_End(self):
        return self._End
    def _get_Budget(self):
        return self._Budget
    def _get_Short(self):
        return self._Short
    def _get_Members(self):
        return self._Members
    def _get_Head(self):
        return self._Head
    def _get_Companies(self):
        return self._CompaniesInvolved
    
    Name = property(_get_Name)
    Start = property(_get_Head)
    ExpectedEnd = property(_get_ExpectedEnd)
    End = property(_get_End)
    Budget = property(_get_Budget)
    Short = property(_get_Short)
    Members = property(_get_Members)
    Head = property(_get_Head)
    CompaniesInvolved = property(_get_Companies)
    def _add_Member(self, member):
        if isinstance(member, (Staff, Internal, External)):
            self.Members.append(member)
            if self not in member.Projects:
                member.add_Project(self)
    def _add_Company(self, company, funding):
        if isinstance(company, Company):
            self._CompaniesInvolved[company] = funding
    def _set_Head(self, head):
        if isinstance(head, Staff):
            self._Head = head
    def _set_End(self, fin):
        self._End = dt.date(int(fin[:4]),int(fin[5:7]), int(fin[8:]))
    def _set_Budget(self, budget):
        self._Budget = budget
    def __repr__(self):
        if len(self._Short) != 0:
            return "{} ({})".format(self._Name,self._Short)
        return self._Name
            
    
class PhD(Project):
    def __init__(self, lenom, une_date_lancement, un_lieu_realisation):
        super().__init__(lenom)
        self._Start = str(une_date_lancement)
        self._DefenseDate = None
        self._Place = str(un_lieu_realisation)
        self._Director = {}
        self._Supervisors = {}
        self._JuryMembers = {}
        self._Project = None
        self._Candidate = ''
    def _get_Name(self):
        return self._Name
    def _get_Start(self):
        return dt.date(int(self._Start[:4]),int(self._Start[5:7]), int(self._Start[8:]))
    def _get_DefenseDate(self):
        return self._DefenseDate
    def _get_Place(self):
        return self._Place
    def _get_Director(self):
        return self._Director
    def _get_Supervisors(self):
        return self._Supervisors
    def _get_JuryMembers(self):
        return self._JuryMembers
    def _get_Project(self):
        return self._Project
    def _get_Candidate(self):
        return self._Candidate
    Name = property(_get_Name)
    Start = property(_get_Start)
    DefenseDate = property(_get_DefenseDate)
    Place = property(_get_Place)
    Director = property(_get_Director)
    Supervisors = property(_get_Supervisors)
    JuryMembers = property(_get_JuryMembers)
    Project = property(_get_Project)
    Candidate = property(_get_Candidate)
    def _set_Director(self, student,rate):
        if isinstance(student, (Staff, Internal, External)):
            if student not in self.Supervisors:
                self._Director = {}
                self._Director[student] = rate
            if student not in student.Projects :
                student.add_Project(self)
    def _add_Supervisor(self, supervisor, rate):
        if isinstance(supervisor, (Staff, Internal, External)):
            self._Supervisors[supervisor] = float(rate)
    def _add_JuryMember(self, jury, role):
            self._JuryMembers[jury] = str(role)
    def _set_Project(self, projet,liste):
        for proj in liste:
            if proj.Name == projet:
                self._Project = proj
                break
    def _set_DefenseDate(self, date):
        if date is str:
            self._DefenseDate = dt.date(int(date[:4]),int(date[5:7]), int(date[8:]))
        else :
            pass
    def _set_Candidate(self, candidate):
        if isinstance(candidate, (Staff, Internal, External)):
            self._Candidate = candidate
    def __repr__(self):
        return self._Name


#articles et projets = type de publications

class Company():
    def __init__(self, lenom):
        self._Name = str(lenom)
    def __repr__(self) :
        return self._Name