from datetime import datetime

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from .models import CustomUser, Post


# ---------------------------------------------------------------------------
# Yordamchi funksiya: dashboard konteksti
# ---------------------------------------------------------------------------

def _dashboard_context(foydalanuvchi):
    bazaviy_qs = Post.objects.filter(user=foydalanuvchi)
    bugun = timezone.localdate()

    jami_vazifalar = bazaviy_qs.count()
    bajarilgan_soni = bazaviy_qs.filter(is_completed=True).count()
    faol_soni = bazaviy_qs.filter(is_completed=False).count()

    kechikkan_qs = bazaviy_qs.filter(
        is_completed=False,
        deadline__date__lte=bugun,
    )
    kechikkan_soni = kechikkan_qs.count()
    kechikkan_vazifalar = kechikkan_qs.order_by('deadline')

    bugungi_vazifalar = bazaviy_qs.filter(
        is_completed=False,
        deadline__date=bugun,
    ).order_by('deadline')

    kelajak_vazifalar = bazaviy_qs.filter(
        is_completed=False,
        deadline__date__gt=bugun,
    ).order_by('deadline')

    arxiv_vazifalar = bazaviy_qs.filter(is_completed=True).order_by('-vaqti')

    bugungi_vazifalar_soni = bugungi_vazifalar.count()
    kelajak_vazifalar_soni = kelajak_vazifalar.count()

    def _foiz(qism, jami):
        if not jami:
            return 0
        return int(round((qism / jami) * 100))

    bajarilish_foizi = _foiz(bajarilgan_soni, jami_vazifalar)
    faol_foizi = _foiz(faol_soni, jami_vazifalar)
    kechikkan_foizi = _foiz(kechikkan_soni, jami_vazifalar)

    profil_maydonlari = [
        foydalanuvchi.first_name,
        foydalanuvchi.last_name,
        foydalanuvchi.email,
        getattr(foydalanuvchi, 'phone_number', None),
        getattr(foydalanuvchi, 'adress', None),
        getattr(foydalanuvchi, 'birth_date', None),
        foydalanuvchi.profile_picture,
    ]
    profil_jami = len(profil_maydonlari)
    profil_tolgan = sum(1 for qiymat in profil_maydonlari if qiymat)
    profil_foiz = _foiz(profil_tolgan, profil_jami)

    return {
        'jami_vazifalar': jami_vazifalar,
        'bajarilgan_soni': bajarilgan_soni,
        'faol_soni': faol_soni,
        'kechikkan_soni': kechikkan_soni,
        'kechikkan_vazifalar': kechikkan_vazifalar,
        'bugungi_vazifalar': bugungi_vazifalar,
        'bugungi_vazifalar_soni': bugungi_vazifalar_soni,
        'kelajak_vazifalar': kelajak_vazifalar,
        'kelajak_vazifalar_soni': kelajak_vazifalar_soni,
        'arxiv_vazifalar': arxiv_vazifalar,
        'bajarilish_foizi': bajarilish_foizi,
        'faol_foizi': faol_foizi,
        'kechikkan_foizi': kechikkan_foizi,
        'profil_jami': profil_jami,
        'profil_tolgan': profil_tolgan,
        'profil_foiz': profil_foiz,
        'bugun': bugun.isoformat(),
    }


# ---------------------------------------------------------------------------
# Dashboard + Profil tahrirlash
# ---------------------------------------------------------------------------

@login_required(login_url='login')
def home_view(request):
    if request.method == 'POST':
        foydalanuvchi = request.user
        foydalanuvchi_nomi = request.POST.get('username', '').strip()
        ism = request.POST.get('first_name', '').strip()
        familiya = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        telefon = request.POST.get('phone_number', '').strip()
        tugilgan_sana = request.POST.get('birth_date', '').strip()
        manzil = request.POST.get('adress', '').strip()
        joriy_parol = request.POST.get('current_password', '').strip()
        yangi_parol = request.POST.get('new_password', '').strip()
        parol_tasdiq = request.POST.get('confirm_password', '').strip()

        # TUZATISH: profil rasm faqat fayl yuborilganda yangilansin
        profil_rasm = request.FILES.get('profile_picture')

        xatolar = []
        parol_ozgardi = False

        if foydalanuvchi_nomi and foydalanuvchi_nomi != foydalanuvchi.username:
            if CustomUser.objects.filter(username=foydalanuvchi_nomi).exclude(pk=foydalanuvchi.pk).exists():
                xatolar.append('Bu username band!')
            else:
                foydalanuvchi.username = foydalanuvchi_nomi

        if email and email != foydalanuvchi.email:
            if CustomUser.objects.filter(email=email).exclude(pk=foydalanuvchi.pk).exists():
                xatolar.append('Bu email band!')
            else:
                foydalanuvchi.email = email

        if telefon and telefon != foydalanuvchi.phone_number:
            if CustomUser.objects.filter(phone_number=telefon).exclude(pk=foydalanuvchi.pk).exists():
                xatolar.append('Bu telefon raqami band!')
            else:
                foydalanuvchi.phone_number = telefon

        # TUZATISH: profil rasm alohida, telefon blokidan tashqarida
        if profil_rasm:
            foydalanuvchi.profile_picture = profil_rasm

        if ism:
            foydalanuvchi.first_name = ism
        if familiya:
            foydalanuvchi.last_name = familiya
        if manzil:
            foydalanuvchi.adress = manzil

        if tugilgan_sana:
            try:
                foydalanuvchi.birth_date = datetime.strptime(tugilgan_sana, '%Y-%m-%d').date()
            except ValueError:
                xatolar.append("Tug'ilgan sana formati noto'g'ri.")

        if joriy_parol or yangi_parol or parol_tasdiq:
            if not (joriy_parol and yangi_parol and parol_tasdiq):
                xatolar.append("Parol maydonlarini to'liq to'ldiring.")
            elif not foydalanuvchi.check_password(joriy_parol):
                xatolar.append("Joriy parol noto'g'ri.")
            elif yangi_parol != parol_tasdiq:
                xatolar.append("Yangi parol va tasdiq mos emas.")
            else:
                try:
                    validate_password(yangi_parol, foydalanuvchi)
                except ValidationError as exc:
                    xatolar.extend(exc.messages)
                else:
                    foydalanuvchi.set_password(yangi_parol)
                    parol_ozgardi = True

        if xatolar:
            kontekst = _dashboard_context(request.user)
            kontekst['postlar'] = Post.objects.filter(user=request.user).order_by('-vaqti')
            kontekst['profil_xato'] = ' '.join(xatolar)
            return render(request, 'base.html', kontekst)

        foydalanuvchi.save()
        if parol_ozgardi:
            update_session_auth_hash(request, foydalanuvchi)

        request.session['profil_muvaffaqiyat'] = "Ma'lumotlar yangilandi."
        return redirect('home_page')

    # GET
    kontekst = _dashboard_context(request.user)
    kontekst['postlar'] = Post.objects.filter(user=request.user).order_by('-vaqti')
    profil_muvaffaqiyat = request.session.pop('profil_muvaffaqiyat', None)
    if profil_muvaffaqiyat:
        kontekst['profil_muvaffaqiyat'] = profil_muvaffaqiyat

    return render(request, 'base.html', kontekst)


# ---------------------------------------------------------------------------
# Vazifa qo'shish
# ---------------------------------------------------------------------------

@login_required(login_url='login')
def qoshish(request):
    if request.method == 'POST':
        sarlavha = request.POST.get('post_title', '').strip()
        matn = request.POST.get('post_text', '').strip()

        if sarlavha and matn:
            muddat_xom = request.POST.get('deadline', '').strip()
            muddat = None
            bajarildi = False

            if muddat_xom:
                muddat = parse_datetime(muddat_xom)
                if muddat is None:
                    try:
                        muddat = datetime.fromisoformat(muddat_xom)
                    except ValueError:
                        muddat = None
                if muddat and timezone.is_naive(muddat):
                    muddat = timezone.make_aware(muddat, timezone.get_current_timezone())
            else:
                bajarildi = True

            Post.objects.create(
                Title=sarlavha,
                Text=matn,
                user=request.user,
                deadline=muddat,
                is_completed=bajarildi,
            )

    return redirect('home_page')


# ---------------------------------------------------------------------------
# Qidiruv
# ---------------------------------------------------------------------------

@login_required(login_url='login')
def qidiruv(request):
    so_rov = request.GET.get('q', '').strip()
    sana_boshlanish = request.GET.get('date_from', '').strip()

    if not so_rov and not sana_boshlanish:
        return redirect('home_page')

    postlar = Post.objects.filter(user=request.user)

    if so_rov:
        postlar = postlar.filter(Q(Title__icontains=so_rov) | Q(Text__icontains=so_rov))

    boshlangan_sana = None
    if sana_boshlanish:
        try:
            boshlangan_sana = datetime.strptime(sana_boshlanish, '%Y-%m-%d').date()
        except ValueError:
            boshlangan_sana = None

    if boshlangan_sana:
        postlar = postlar.filter(vaqti__date__gte=boshlangan_sana)

    postlar = postlar.order_by('-vaqti')

    kontekst = _dashboard_context(request.user)
    kontekst.update({
        'postlar': postlar,
        'qidiruv': so_rov,
        'topilmadi': not postlar.exists(),
    })

    return render(request, 'base.html', kontekst)


# ---------------------------------------------------------------------------
# Vazifani tasdiqlash (bajarildi)
# ---------------------------------------------------------------------------

@login_required(login_url='login')
def tasdiqlash(request, id):
    if request.method == 'POST':
        vazifa = get_object_or_404(Post, id=id, user=request.user)
        if not vazifa.is_completed:
            vazifa.is_completed = True
            vazifa.save(update_fields=['is_completed'])
    return redirect('home_page')


# ---------------------------------------------------------------------------
# Vazifani o'chirish
# ---------------------------------------------------------------------------

@login_required(login_url='login')
def ochirish(request, id):
    if request.method == 'POST':
        vazifa = get_object_or_404(Post, id=id, user=request.user)
        vazifa.delete()
    return redirect('home_page')


# ---------------------------------------------------------------------------
# Vazifani yangilash
# ---------------------------------------------------------------------------

@login_required(login_url='login')
def yangilash(request):
    if request.method == 'POST':
        yozuv_id = request.POST.get('post_id')
        sarlavha_tahrir = request.POST.get('edit_title', '').strip()
        matn_tahrir = request.POST.get('edit_text', '').strip()

        if sarlavha_tahrir and matn_tahrir and yozuv_id:
            tanlangan_vazifa = get_object_or_404(Post, id=yozuv_id, user=request.user)
            tanlangan_vazifa.Title = sarlavha_tahrir
            tanlangan_vazifa.Text = matn_tahrir
            tanlangan_vazifa.save(update_fields=['Title', 'Text'])

    return redirect('home_page')


# ---------------------------------------------------------------------------
# Login / Logout / Ro'yxatdan o'tish
# ---------------------------------------------------------------------------

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home_page')

    if request.method == 'POST':
        foydalanuvchi_nomi = request.POST.get('username', '').strip()
        parol = request.POST.get('password', '')
        foydalanuvchi = authenticate(request, username=foydalanuvchi_nomi, password=parol)

        if foydalanuvchi is not None:
            login(request, foydalanuvchi)
            return redirect('home_page')
        else:
            return render(request, 'login.html', {'xato': True})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def registry(request):
    if request.user.is_authenticated:
        return redirect('home_page')

    if request.method == 'POST':
        ism = request.POST.get('first_name', '').strip()
        familiya = request.POST.get('last_name', '').strip()
        foydalanuvchi_nomi = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        telefon = request.POST.get('phone', '').strip()
        tugilgan_sana = request.POST.get('birth_date', '').strip()
        manzil = request.POST.get('address', '').strip()
        parol = request.POST.get('password', '')
        parol_tasdiq = request.POST.get('confirm_password', '')

        malumotlar = [ism, familiya, foydalanuvchi_nomi, email, telefon, tugilgan_sana, manzil, parol, parol_tasdiq]

        if not all(malumotlar):
            return render(request, 'signup.html', {'xato': "Barcha ma'lumotlarni to'ldiring!"})

        if parol != parol_tasdiq:
            return render(request, 'signup.html', {'xato': 'Kiritilgan parollar bir-biriga mos emas!'})

        if CustomUser.objects.filter(username=foydalanuvchi_nomi).exists():
            return render(request, 'signup.html', {'xato': 'Bu username band!'})

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'xato': 'Bu email band!'})

        if CustomUser.objects.filter(phone_number=telefon).exists():
            return render(request, 'signup.html', {'xato': 'Bu telefon raqami band!'})

        # Parolni validatsiya qilish
        try:
            temp_user = CustomUser(username=foydalanuvchi_nomi)
            validate_password(parol, temp_user)
        except ValidationError as exc:
            return render(request, 'signup.html', {'xato': ' '.join(exc.messages)})

        CustomUser.objects.create_user(
            username=foydalanuvchi_nomi,
            email=email,
            password=parol,
            first_name=ism,
            last_name=familiya,
            phone_number=telefon,
            birth_date=tugilgan_sana or None,
            adress=manzil,
        )

        return render(request, 'signup.html', {'muvaffaqiyat': True})

    return render(request, 'signup.html')

def chiqaradi(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    return render(request, 'landing.html')