from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from users.models import Users
from courses.models import Courses
from enrollments.models import Enrollments
from myauth.mixins import MentorRequiredMixin, StudentRequiredMixin

# Create your views here.
"""
class EnrollmentView(LoginRequiredMixin, View):

    def get(self, request, extra_context=None, *args, **kwargs):
        template_name = 'enrollments/enrollment-view.html'
        context = {}

        print(request.method, " iz get()")

        current_user = Users.objects.get(id=request.user.id)
        print(current_user.user_role, "user_role trenutnog usera")

        # ako je student zatrazio stranicu onda direktno dohvatim njegove podatke za upisni list
        # nema sanse da vidi podatke nekog drugog studenta
        if current_user.user_role == 'STUDENT':
            try:
                if kwargs['url_student_id']:
                    print(kwargs['url_student_id'])
                    print(self.kwargs['url_student_id'])
                    return redirect('enrollment')
            except KeyError:
                print("url param does not exist OK")

            # predmeti_svi = Courses.objects.all()
            # upisani = Enrollments.objects.filter(student_id=request.user.id).order_by('predmet_id_id')
            upisani = Enrollments.objects.filter(student_id=current_user.id).order_by('predmet_id_id')
            neupisani = Courses.objects.exclude(id__in=upisani.values('predmet_id')).order_by('ime')
            print("###########")
            print(upisani)
            print(upisani.filter(predmet_id=7, student_id=2))
            # print(upisani.filter(predmet_id=7, student_id=2)[0].status)  # baca error ako ne postoji, list index out of range

            upisani2 = Courses.objects.exclude(id__in=neupisani.values('id')).order_by('ime')
            upisani3 = Courses.objects.exclude(id__in=neupisani.values('id')).order_by('ime')

            br_semestara = 6 if current_user.status == 'REDOVNI' else 8
            print(br_semestara, "broj semestara")

            predmeti_po_semestrima = list()
            for x in range(0, br_semestara):
                predmeti_po_semestrima.append(list())
                for predmet in upisani2:
                    #print(predmet)
                    #print(predmet.sem_redovni)
                    if predmet.sem_redovni == x + 1:
                        predmeti_po_semestrima[x].append(predmet)

            predmeti_po_semestrima3 = list()
            for x in range(0, br_semestara):
                predmeti_po_semestrima3.append(dict())
                for predmet in upisani2:
                    #print(predmet)
                    #print(predmet.sem_redovni)
                    if predmet.sem_redovni == x + 1:
                        if upisani.filter(predmet_id=predmet.id, student_id=current_user.id):
                            predmeti_po_semestrima3[x][predmet] = upisani.filter(predmet_id=predmet.id,
                                                                                 student_id=current_user.id)[0].status
            print(predmeti_po_semestrima3)

            #print(predmeti_po_semestrima)

            context['not_enrolled_courses'] = neupisani
            context['count1'] = neupisani.count()
            context['requested_student_email'] = current_user.email
            context['br_semestara'] = range(1, br_semestara + 1)
            context['br_semestara2'] = br_semestara
            context['enrolled_courses'] = predmeti_po_semestrima
            context['enrolled_courses3'] = predmeti_po_semestrima3

            if extra_context:
                context['confirmation'] = extra_context['confirmation']

            return render(request, template_name, context)

        # ako je mentor zatrazio stranicu, onda je u url potrebno da dode <int> kao parametar
        # onda sa tim parametrom provjerim dali user postoji i jel student,
        elif current_user.user_role == 'MENTOR':
            try:
                if kwargs['url_student_id']:
                    print(kwargs['url_student_id'])
                    print(self.kwargs['url_student_id'])
            except KeyError:
                print("url param does not exist")
                return redirect('students')

            try:
                requested_student = Users.objects.get(id=int(kwargs['url_student_id']))
                print("user dohvacen")
                if requested_student.user_role != 'STUDENT':
                    return redirect('students')

            except Users.DoesNotExist:
                print("user ne postoji")
                return redirect('students')


            upisani = Enrollments.objects.filter(student_id=requested_student.id).order_by('predmet_id_id')
            neupisani = Courses.objects.exclude(id__in=upisani.values('predmet_id')).order_by('ime')

            upisani2 = Courses.objects.exclude(id__in=neupisani.values('id')).order_by('ime')

            br_semestara = 6 if current_user.status == 'REDOVNI' else 8
            print(br_semestara, "broj semestara")

            predmeti_po_semestrima = list()
            for x in range(0, br_semestara):
                predmeti_po_semestrima.append(list())
                for predmet in upisani2:
                    #print(predmet)
                    #print(predmet.sem_redovni)
                    if predmet.sem_redovni == x + 1:
                        predmeti_po_semestrima[x].append(predmet)

            predmeti_po_semestrima3 = list()
            for x in range(0, br_semestara):
                predmeti_po_semestrima3.append(dict())
                for predmet in upisani2:
                    # print(predmet)
                    # print(predmet.sem_redovni)
                    if predmet.sem_redovni == x + 1:
                        if upisani.filter(predmet_id=predmet.id, student_id=requested_student.id):
                            predmeti_po_semestrima3[x][predmet] = upisani.filter(predmet_id=predmet.id,
                                                                                 student_id=requested_student.id)[0].status

            context['not_enrolled_courses'] = neupisani
            context['count1'] = neupisani.count()
            context['requested_student_email'] = requested_student.email
            context['br_semestara'] = range(1, br_semestara + 1)
            context['br_semestara2'] = br_semestara
            context['enrolled_courses'] = predmeti_po_semestrima
            context['enrolled_courses3'] = predmeti_po_semestrima3

            return render(request, template_name, context)



    def post(self, request, *args, **kwargs):
        print(request.method, " iz post()")

        template_name = 'enrollments/enrollment-view.html'
        extra_context = {}

        if request.POST.get('enroll'):
            predmet_id = request.POST.get('enroll')
            print(predmet_id)

            url_student_id = None
            try:
                url_student_id = kwargs['url_student_id']
            except KeyError:
                print("nema url parametra")

            try:
                predmet_id_cleaned = int(predmet_id)
                print(predmet_id_cleaned)
                #print(kwargs['url_student_id'], "url iz kwargs, u post enroll")
                # upisivanje predmeta
                print(request.user.id, "user id")

                # ako je student logiran
                if request.user.user_role == 'STUDENT':
                    print("trenutno studetn logiran")
                    current_student = Users.objects.get(id=request.user.id)
                    try:
                        requested_course = Courses.objects.get(id=predmet_id_cleaned)
                    except Courses.DoesNotExist:
                        print("course does not exist")
                        return redirect('students')
                    if not Enrollments.objects.filter(student_id_id=current_student.id,
                                                      predmet_id_id=requested_course.id):
                        Enrollments.objects.create(student_id_id=current_student.id,
                                                   predmet_id_id=requested_course.id,
                                                   status='enrolled')
                        extra_context['confirmation'] = "Subject added!"
                        extra_context['clicked_subject_id'] = predmet_id_cleaned

                # ako je mentor logiran
                else:
                    if url_student_id:
                        try:
                            requested_student = Users.objects.get(id=int(kwargs['url_student_id']))
                            print("user dohvacen")
                            if requested_student.user_role != 'STUDENT':
                                return redirect('students')
                            requested_course = Courses.objects.get(id=predmet_id_cleaned)

                        except Users.DoesNotExist:
                            print("user ne postoji")
                            return redirect('students')
                        except Courses.DoesNotExist:
                            print("course does not exist")
                            return redirect('students')
                    else:
                        return redirect('studenti')

                    # ako predmet nije upisan, upisujemo ga
                    if not Enrollments.objects.filter(student_id_id=requested_student.id,
                                                      predmet_id_id=requested_course.id):
                        Enrollments.objects.create(student_id_id=requested_student.id,
                                                   predmet_id_id=requested_course.id,
                                                   status='enrolled')
                        extra_context['confirmation'] = "Subject added!"
                        extra_context['clicked_subject_id'] = predmet_id_cleaned
                    else:
                        # ovo mi i ne treba jer svejedno na listi imam samo neupisane predmete
                        extra_context['confirmation'] = "Subject already enrolled!"

            except ValueError:
                print("Input is not int!")
            except KeyError:
                print("KeyError nema url-a")

        elif request.POST.get('mark_dissenrolled'):
            predmet_id = request.POST.get('mark_dissenrolled')
            url_student_id = None
            try:
                url_student_id = kwargs['url_student_id']
            except KeyError:
                print("nema url parametra")

            try:
                predmet_id_cleaned = int(predmet_id)
            except ValueError:
                predmet_id("id nije int")

            if request.user.user_role == 'STUDENT':
                current_student = Users.objects.get(id=request.user.id)
                try:
                    requested_course = Courses.objects.get(id=predmet_id_cleaned)
                except Courses.DoesNotExist:
                    print("course does not exist")
                    return redirect('students')
                if Enrollments.objects.filter(student_id_id=current_student.id,
                                              predmet_id_id=requested_course.id):
                    Enrollments.objects.filter(student_id_id=current_student.id,
                                               predmet_id_id=requested_course.id,).delete()

            else:
                if url_student_id:
                    try:
                        requested_student = Users.objects.get(id=int(kwargs['url_student_id']))
                        print("user dohvacen")
                        if requested_student.user_role != 'STUDENT':
                            return redirect('students')
                        requested_course = Courses.objects.get(id=predmet_id_cleaned)

                    except Users.DoesNotExist:
                        print("user ne postoji")
                        return redirect('students')
                    except Courses.DoesNotExist:
                        print("course does not exist")
                        return redirect('students')
                else:
                    return redirect('students')

                if Enrollments.objects.filter(student_id_id=requested_student.id,
                                              predmet_id_id=requested_course.id):
                    Enrollments.objects.filter(student_id_id=requested_student.id,
                                               predmet_id_id=requested_course.id,).delete()

        elif request.POST.get('mark_passed'):
            print('$$$$$$$$ post mark_passed')
            predmet_id = request.POST.get('mark_passed')
            url_student_id = None
            try:
                url_student_id = kwargs['url_student_id']
            except KeyError:
                print("nema url parametra")

            try:
                predmet_id_cleaned = int(predmet_id)
            except ValueError:
                predmet_id("id nije int")

            # mislim da sam ovdje isao na shemu da nije bitan user_role
            # vec bi samo overridao requested_student ako postoji url_student_id
            # sto bi znacilo da se radio o mentoru,
            # a to mogu napraviti jer editam isto objekt u bazi neovisno o tome
            # koji user to mijenja...
            # ... ovo je dobra ideja mozda za neke preformanse (iako ovaj dio koda
            # sveukupno nije dobar primjer) ali je pre tesko pratiti kod na ovaj nacin
            # tako da je bolje ovako ne raditi
            if request.user.user_role == 'MENTOR' or 'STUDENT':
                requested_student = Users.objects.get(id=request.user.id)
                requested_course = Courses.objects.get(id=predmet_id_cleaned) # ovo nije dobro moram u try stavit
                if url_student_id:
                    try:
                        requested_student = Users.objects.get(id=int(kwargs['url_student_id']))
                        print("user dohvacen")
                        if requested_student.user_role != 'STUDENT':
                            return redirect('students')
                        requested_course = Courses.objects.get(id=predmet_id_cleaned)

                    except Users.DoesNotExist:
                        print("user ne postoji")
                        return redirect('students')
                    except Courses.DoesNotExist:
                        print("course does not exist")
                        return redirect('students')
                else:
                    pass
                    #return redirect('students')

                print('$$$$$$$$')
                if Enrollments.objects.filter(student_id_id=requested_student.id,
                                              predmet_id_id=requested_course.id):
                    Enrollments.objects.filter(student_id_id=requested_student.id,
                                               predmet_id_id=requested_course.id,).update(status='passed')



        print("ovdje nastavljamo")

        # return render(request, template_name, context)
        return self.get(request, extra_context=extra_context, *args, **kwargs)
"""

# vazna stvar
# trebalo bi provjeravati s kojim predmetima se smije sto radit (upis, ispis, polozeno, nepolozeno)
# iako s user_role dolaze ovlasti, to ne znaci da smijem dopustiti sve nad svakim predmetom
# npr. ako je predmet polozen, ajmo rec da se onda vise ne moze oznaciti da je nepolozen ili nesto drugo
# ja bi mogao unutar html forme za mark_dissenrolled editirat id nekog drugog predmeta i staviti id polozenog
# predmeta a sumbitat formu i onda bi polozeni predmet opet bio neupisan...
# u tom slucaju svaki put kada bi mijenjao status upisa treba provjeriti koji je trenutni status i onda odluciti jel
# se smije mijenjati...

# vazno za Mixins
# Najbolje je da mi "zadnja" view klasa nasljeduje mixine
# tako mogu lako pratiti kako ce se sto izvrsavati
# ja sam ovdje ispod napravi baznu klasu EnrollmentBaseView(LoginRequiredMixin, View):
# pa sam onda napravio klasu EnrollmentMentorView(MentorRequiredMixin, EnrollmentBaseView):
# medutim prije se izvrsio MentorRequiredMixin nego LoginRequiredMixin sto nije bila namjena
# posljedica je to sto bi pukao program jer MentorRequiredMixin zadtjeva da je LoginRequiredMixin zadovoljen
# bila je jos jedna ideja
# EnrollmentBaseView(LoginRequiredMixin, View):
# EnrollmentMentorView(EnrollmentBaseView, MentorRequiredMixin):
# staviti MentorRequiredMixin iza, medutim to ne moze
# zbog toga sto moj mixin overrida dispatch() metodu, a posto sam je sada "zadnju" nasljedio tj.
# u nasljedivanju je skroz desno, ovaj LoginRequiredMixin se prvi izvrsi, a njegov kod je takav da ako
# je uvjet zadovoljen pozvat ce se super dispatch metoda koja je dispatc metoda iz View i view ce se renderat
# a moj MentorRequiredMixin se neci niti izvrsiti


class EnrollmentBaseView(View):
    def get_url_param(self, *args, **kwargs):
        try:
            if kwargs['url_student_id']:
                print(kwargs['url_student_id'])
                print(self.kwargs['url_student_id'])
                return kwargs['url_student_id']
        except KeyError:
            print("Url parameter does not exist - student view OK")
            return None

    def get_requested_student(self, student_id, *args, **kwargs):
        # ovdje bi bilo dobro provjeriti dali je student_id tipa int
        # ali ovaj put nema potrebe jer je u urls, putanji definirano da treba biti int (<int:id>)
        try:
            student = Users.objects.get(id=student_id)
            if student.user_role == 'STUDENT':
                return student
            else:
                return None
        except Users.DoesNotExist:
            return None

    def get_course(self, course_id):
        try:
            print("$$$$$", course_id)
            cleaned_id = int(course_id)
        except ValueError:
            # id nije tipa int
            return None
        try:
            course = Courses.objects.get(id=cleaned_id)
            return course
        except Courses.DoesNotExist:
            return None

    def broj_semestara(self, user, *args, **kwargs):
        # user je tipa Users, object iz baze
        if user.status == 'REDOVNI':
            return 6
        else:
            return 8

    def predmeti_po_semestrima(self, user_id, *args, **kwargs):
        user = Users.objects.get(id=user_id)

        # mislim da postoji bolji nacin dohvacanja upisanih predemta...
        # model Enrollments
        upisni_list = Enrollments.objects.filter(student_id=user.id).order_by('predmet_id_id')

        # model Courses
        neupisani_predmeti = Courses.objects.exclude(id__in=upisni_list.values('predmet_id')).order_by('ime')
        upisani_predmeti = Courses.objects.exclude(id__in=neupisani_predmeti.values('id')).order_by('ime')

        predmeti_po_semestrima = list()
        for x in range(0, self.broj_semestara(user)):
            predmeti_po_semestrima.append(dict())
            for predmet in upisani_predmeti:
                if predmet.sem_redovni == x + 1:
                    if upisni_list.filter(predmet_id=predmet.id,
                                          student_id=user.id):
                        predmeti_po_semestrima[x][predmet] = upisni_list.filter(predmet_id=predmet.id,
                                                                                student_id=user.id)[0].status

        # return-am listu dictionary-a, key je Course, value je status(passed, enrolled...)
        # i return-am neupisane predmete
        return predmeti_po_semestrima, neupisani_predmeti


class EnrollmentStudentView(LoginRequiredMixin, StudentRequiredMixin, EnrollmentBaseView):
    def is_status_edit_valid(self, predmet_id, user_id, **kwargs):
        if not self.get_course(predmet_id):
            return False, None, None
        course = self.get_course(predmet_id)
        user = Users.objects.get(id=user_id)
        return True, user, course

    def get(self, request, message=None, *args, **kwargs):
        template_name = 'enrollments/enrollment-view_new.html'
        context = {}

        current_student = Users.objects.get(id=request.user.id)

        # redirectam usera (Studenta) jer mu nije dozvoljeno da pristupa view-u s parametrima u url
        if self.get_url_param():
            return redirect('enrollment')

        predmeti_po_semestrima, neupisani = self.predmeti_po_semestrima(current_student.id)

        context['enrolled_courses'] = predmeti_po_semestrima
        context['not_enrolled_courses'] = neupisani
        context['requested_student_email'] = current_student.email
        context['br_semestara'] = self.broj_semestara(current_student)

        context['msg'] = message

        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        template_name = 'enrollments/enrollment-view_new.html'

        message = None

        if request.POST.get('enroll'):
            _, current_user, course = self.is_status_edit_valid(request.POST.get('enroll'), request.user.id)

            # zadatak
            # oop id je 20
            # id 51 mobilne teh.
            if course.id == 51:
                if Enrollments.objects.filter(predmet_id_id=20, student_id_id=current_user.id,
                                           status='passed'):
                    if not _:
                        return self.get(request, *args, **kwargs)
                    if not Enrollments.objects.filter(student_id_id=current_user.id, predmet_id_id=course.id):
                        Enrollments.objects.create(student_id_id=current_user.id, predmet_id_id=course.id, status='enrolled')
                else:
                    message = "Nemozete upisati Mobilne tehnologije jer nemate polozeno OOP"
            else:
                if not _:
                    return self.get(request, *args, **kwargs)
                if not Enrollments.objects.filter(student_id_id=current_user.id, predmet_id_id=course.id):
                    Enrollments.objects.create(student_id_id=current_user.id, predmet_id_id=course.id, status='enrolled')

            """
            if not _:
                return self.get(request, *args, **kwargs)
            if not Enrollments.objects.filter(student_id_id=current_user.id, predmet_id_id=course.id):
                Enrollments.objects.create(student_id_id=current_user.id, predmet_id_id=course.id,status='enrolled')
            """

        elif request.POST.get('mark_dissenrolled'):
            _, current_user, course = self.is_status_edit_valid(request.POST.get('mark_dissenrolled'), request.user.id)
            if not _:
                return self.get(request, *args, **kwargs)
            if Enrollments.objects.filter(student_id_id=current_user.id, predmet_id_id=course.id):
                Enrollments.objects.filter(student_id_id=current_user.id, predmet_id_id=course.id).delete()

        elif request.POST.get('mark_passed'):
            _, current_user, course = self.is_status_edit_valid(request.POST.get('mark_passed'), request.user.id)
            if not _:
                return self.get(request, *args, **kwargs)
            if Enrollments.objects.filter(student_id_id=current_user.id, predmet_id_id=course.id):
                Enrollments.objects.filter(student_id_id=current_user.id, predmet_id_id=course.id).update(status='passed')

        elif request.POST.get('mark_unpassed'):
            _, current_user, course = self.is_status_edit_valid(request.POST.get('mark_unpassed'), request.user.id)
            if not _:
                return self.get(request, *args, **kwargs)
            if Enrollments.objects.filter(student_id_id=current_user.id, predmet_id_id=course.id):
                Enrollments.objects.filter(student_id_id=current_user.id, predmet_id_id=course.id).update(status='enrolled')

        return self.get(request, message, *args, **kwargs)
        # return redirect('enrollments')


class EnrollmentMentorView(LoginRequiredMixin, MentorRequiredMixin, EnrollmentBaseView):
    def is_status_edit_valid(self, predmet_id, **kwargs):
        if not self.get_course(predmet_id):
            return False, None, None
        if not self.get_url_param(**kwargs):
            self.get_url_param(**kwargs)
        student = self.get_requested_student(self.get_url_param(**kwargs))
        course = self.get_course(predmet_id)
        return True, student, course

    def get(self, request, *args, **kwargs):
        template_name = 'enrollments/enrollment-view_new.html'
        context = {}

        current_user = Users.objects.get(id=request.user.id)

        # ako ne postoji url int:id parametar onda ga prebacujem na drugi view
        if not self.get_url_param(**kwargs):
            return redirect('students')

        student_id_from_url = self.get_url_param(**kwargs)
        requested_student = self.get_requested_student(student_id_from_url)

        if requested_student is None:
            return redirect('students')

        predmeti_po_semestrima, neupisani = self.predmeti_po_semestrima(requested_student.id)

        context['enrolled_courses'] = predmeti_po_semestrima
        context['not_enrolled_courses'] = neupisani
        context['requested_student_email'] = requested_student.email
        context['br_semestara'] = self.broj_semestara(requested_student)

        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        template_name = 'enrollments/enrollment-view_new.html'

        if request.POST.get('enroll'):
            _, requested_student, course = self.is_status_edit_valid(request.POST.get('enroll'), **kwargs)
            if not _:
                return self.get(request, *args, **kwargs)
            if not Enrollments.objects.filter(student_id_id=requested_student.id, predmet_id_id=course.id):
                Enrollments.objects.create(student_id_id=requested_student.id, predmet_id_id=course.id, status='enrolled')

        elif request.POST.get('mark_dissenrolled'):
            _, requested_student, course = self.is_status_edit_valid(request.POST.get('mark_dissenrolled'), **kwargs)
            if not _:
                return self.get(request, *args, **kwargs)
            if Enrollments.objects.filter(student_id_id=requested_student.id, predmet_id_id=course.id):
                Enrollments.objects.filter(student_id_id=requested_student.id, predmet_id_id=course.id).delete()

        elif request.POST.get('mark_passed'):
            _, requested_student, course = self.is_status_edit_valid(request.POST.get('mark_passed'), **kwargs)
            if not _:
                return self.get(request, *args, **kwargs)
            if Enrollments.objects.filter(student_id_id=requested_student.id, predmet_id_id=course.id):
                Enrollments.objects.filter(student_id_id=requested_student.id, predmet_id_id=course.id).update(status='passed')

        elif request.POST.get('mark_unpassed'):
            _, requested_student, course = self.is_status_edit_valid(request.POST.get('mark_unpassed'), **kwargs)
            if not _:
                return self.get(request, *args, **kwargs)
            if Enrollments.objects.filter(student_id_id=requested_student.id, predmet_id_id=course.id):
                Enrollments.objects.filter(student_id_id=requested_student.id, predmet_id_id=course.id).update(status='enrolled')

        return self.get(request, *args, **kwargs)


# svi predemti s vise od 6 ects, koje je upisao barem 1 student
# ako ne postoju ispise se ne postoji
class View1(LoginRequiredMixin, MentorRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        template_name = 'enrollments/custom1.html'
        context = {}

        upisni_listovi = Enrollments.objects.filter(status='enrolled')
        result = Courses.objects.filter(id__in=upisni_listovi.values('predmet_id_id'), bodovi__gte=6).order_by('kod')

        # drugi nacin
        predmeti = Courses.objects.filter(bodovi__gte=6).order_by('kod')
        # x = Enrollments.objects.filter(predmet_id_id=30).first()  # vraca prvog ili None, (meze i last())
        # print(x)
        for p in predmeti:
            if Enrollments.objects.filter(predmet_id_id=p.id, status='enrolled').first() is not None:
                predmeti.exclude(id=p.id)

        if result.count() == 0:
            context['result'] = "nema rezultata"
            context['r1_count'] = 0
        else:
            context['result'] = result
            context['r1_count'] = result.count()
            context['result2'] = predmeti
            context['r2_count'] = predmeti.count()

        return render(request, template_name, context)

class View2(View):
    def get(self, request, *args, **kwargs):
        template_name = 'enrollments/custom2.html'
        context = {}

        oop = Courses.objects.get(kod='SIT020')
        result = list()

        result.append(list())  # redovni
        result.append(list())  # izvanredni

        upisni_listovi = Enrollments.objects.filter(predmet_id_id=oop.id, status='passed')
        print(upisni_listovi)

        for x in upisni_listovi:
            print(x.student_id_id)
            if Users.objects.filter(id=x.student_id_id, status='REDOVNI').first():
                result[0].append(Users.objects.get(id=x.student_id_id))
            elif Users.objects.filter(id=x.student_id_id, status='IZVANREDNI').first():
                result[1].append(Users.objects.get(id=x.student_id_id))

        print(result)

        context['studenti'] = result
        context['red'] = result[0]
        context['izv'] = result[1]
        context['redc'] = len(result[0])
        context['izvc'] = len(result[1])

        return render(request, template_name, context)

class View2detail(View):
    def get(self, request, *args, **kwargs):
        template_name = 'enrollments/custom2detail.html'
        context = {}

        oop = Courses.objects.get(kod='SIT020')
        result = list()

        result.append(list())  # redovni
        result.append(list())  # izvanredni

        upisni_listovi = Enrollments.objects.filter(predmet_id_id=oop.id, status='passed')
        print(upisni_listovi)

        for x in upisni_listovi:
            print(x.student_id_id)
            if Users.objects.filter(id=x.student_id_id, status='REDOVNI').first():
                result[0].append(Users.objects.get(id=x.student_id_id))
            elif Users.objects.filter(id=x.student_id_id, status='IZVANREDNI').first():
                result[1].append(Users.objects.get(id=x.student_id_id))

        print(result)

        print(self.kwargs['s'])

        if self.kwargs['s'] == 'r':
            context['studenti'] = result[0]

        elif self.kwargs['s'] == 'i':
            context['studenti'] = result[1]

        """
        context['studenti'] = result
        context['red'] = result[0]
        context['izv'] = result[1]
        context['redc'] = len(result[0])
        context['izvc'] = len(result[1])
        """

        return render(request, template_name, context)
