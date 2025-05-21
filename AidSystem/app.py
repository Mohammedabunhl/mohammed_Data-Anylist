from flask import Flask, render_template, request, redirect, send_file, url_for, session, flash, jsonify
import mysql.connector
from datetime import datetime
import pandas as pd
from io import BytesIO
import timeago

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# إعداد الاتصال مع MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="120200885",
    database="aid_system"
)
cursor = db.cursor(dictionary=True)

# صفحة تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            session['user'] = user['username']
            session['role'] = user['role']  # تخزين الدور في السيشن
            save_notification(f"تم تسجيل دخول المستخدم: {user['username']}")
            return redirect(url_for('dashboard'))
        else:
            flash("خطأ في اسم المستخدم أو كلمة المرور")

    return render_template('login.html')



@app.template_filter('format_datetime')
def format_datetime(value, format='%Y-%m-%d %H:%M'):
    if isinstance(value, datetime):
        return value.strftime(format)
    return value


from datetime import datetime
# تأكد من استيراد مكتبة timeago_lib أو استبدلها بالمكتبة التي تستخدمها
# import timeago_lib 

@app.template_filter('timeago')
def timeago_filter(value):
    now = datetime.now()

    if isinstance(value, datetime):
        return timeago.format(value, now, locale='ar')

    formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]  # أضفنا صيغة بدون ثواني

    for fmt in formats:
        try:
            parsed_date = datetime.strptime(value, fmt)
            return timeago.format(parsed_date, now, locale='ar')
        except:
            continue

    return "تاريخ غير صالح"
    



# الصفحة الرئيسية

def safe_format_date(date_value):
    """
    ترجع تاريخ منسق من مدخل قد يكون نص أو datetime أو None.
    """
    if date_value is None:
        return 'N/A'
    
    if isinstance(date_value, datetime):
        return date_value.strftime('%Y-%m-%d %H:%M')
    
    if isinstance(date_value, str):
        # جرب أكثر من صيغة معروفة للتاريخ
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d'):
            try:
                dt = datetime.strptime(date_value, fmt)
                return dt.strftime('%Y-%m-%d %H:%M')
            except ValueError:
                continue
        # لو فشل التحويل لكل الصيغ
        return 'N/A'
    
    # لأي نوع غير متوقع
    return 'N/A'

@app.route('/')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    user_role = session.get('role', 'user')

    cursor.execute("""
        SELECT name_male, national_id_1, phone_number, family_members, aid_type, created_at
        FROM beneficiaries
    """)
    raw_data = cursor.fetchall()
    data = []
    for row in raw_data:
        created_at = safe_format_date(row.get('created_at'))
        data.append({
            'name_male': row.get('name_male'),
            'national_id_1': row.get('national_id_1'),
            'phone_number': row.get('phone_number'),
            'family_members': row.get('family_members'),
            'aid_type': row.get('aid_type'),
            'created_at': created_at
        })

    cursor.execute("SELECT COUNT(*) AS unread FROM notifications WHERE is_read = 0")
    unread_result = cursor.fetchone()
    unread_count = unread_result['unread'] if unread_result else 0

    cursor.execute("""
        SELECT message, created_at, is_read
        FROM notifications
        ORDER BY created_at DESC
        LIMIT 10
    """)
    raw_notifications = cursor.fetchall()
    notifications = []
    for notif in raw_notifications:
        created_at = safe_format_date(notif.get('created_at'))
        notifications.append({
            'message': notif.get('message'),
            'created_at': created_at,
            'is_read': notif.get('is_read')
        })

    return render_template('dashboard.html', data=data, notifications=notifications, unread_count=unread_count, user_role=user_role)

@app.route('/export', methods=['POST'])
def export_to_excel():
    if 'user' not in session:
        return redirect(url_for('login'))

    # فقط الأدمن يستطيع التصدير (مثال)
    if session.get('role') != 'admin':
        flash("غير مصرح لك بتصدير البيانات")
        return redirect(url_for('dashboard'))

    cursor.execute("""
        SELECT name_male AS 'الاسم',
               national_id_1 AS 'رقم الهوية',
               phone_number AS 'رقم الجوال',
               family_members AS 'عدد الأفراد',
               aid_type AS 'نوع المساعدة',
               created_at AS 'تاريخ التسليم'
        FROM beneficiaries
        ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows)

    if 'تاريخ التسليم' in df.columns:
        df['تاريخ التسليم'] = pd.to_datetime(df['تاريخ التسليم'], errors='coerce').dt.strftime('%Y-%m-%d')

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='المستفيدين', index=False)

    output.seek(0)
    return send_file(output, download_name='المستفيدين.xlsx', as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


# إضافة مستفيد

@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # البيانات الأساسية
        national_id_1 = request.form['national_id_1']
        name_male = request.form['name_male']
        phone_number = request.form['phone_number']
        family_members = request.form['family_members']
        family_members_injured = request.form['family_members_injured']
        injured = request.form['injured']
        damage_status = request.form['damage_status']
        marital_status = request.form['marital_status']
        wives_count = request.form.get('wives_count')
        Resident_displaced = request.form['Resident_displaced']
        notes = request.form.get('notes') or None

        # الزوجة 1
        name_female = request.form.get('name_female') or None
        national_id_2 = request.form.get('national_id_2') or None

        # زوجات إضافيات
        wife2_name = request.form.get('wife2_name') or None
        wife2_national_id = request.form.get('wife2_national_id') or None
        wife3_name = request.form.get('wife3_name') or None
        wife3_national_id = request.form.get('wife3_national_id') or None
        wife4_name = request.form.get('wife4_name') or None
        wife4_national_id = request.form.get('wife4_national_id') or None

        # المساعدة
        aid_type = request.form['aid_type']
        aid_amount = request.form.get('aid_amount')
        aid_amount = float(aid_amount) if aid_amount else None
        other_type_help = request.form.get('other_type_help') or None

        # بيانات إضافية
        area = request.form.get('area') or None
        landmark = request.form.get('landmark') or None
        gender = request.form.get('gender') or None

        # تنفيذ الإدخال
        cursor.execute("""
            INSERT INTO beneficiaries (
                national_id_1, name_male, national_id_2, name_female,
                wife2_name, wife2_national_id,
                wife3_name, wife3_national_id,
                wife4_name, wife4_national_id,
                phone_number, family_members, family_members_injured,
                injured, damage_status, marital_status, wives_count,
                aid_type, aid_amount, other_type_help, notes,
                created_at, area, landmark, gender,Resident_displaced
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s,%s)
        """, (
            national_id_1, name_male, national_id_2, name_female,
            wife2_name, wife2_national_id,
            wife3_name, wife3_national_id,
            wife4_name, wife4_national_id,
            phone_number, family_members, family_members_injured,
            injured, damage_status, marital_status, wives_count,
            aid_type, aid_amount, other_type_help, notes,
            datetime.now(), area, landmark, gender, Resident_displaced
        ))

        db.commit()
        flash("تمت الإضافة بنجاح")
        save_notification(f"تمت إضافة مستفيد: {name_male}")
        return redirect(url_for('dashboard'))

    return render_template('add.html')



# تعديل مستفيد
@app.route('/edit/<national_id>', methods=['GET', 'POST'])
def edit_beneficiary(national_id):
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        name_male = request.form['name_male']
        name_female = request.form['name_female']
        national_id_1 = request.form['national_id_1']
        national_id_2 = request.form['national_id_2']
        phone_number = request.form['phone_number']
        family_members = request.form['family_members']
        family_members_injured = request.form['family_members_injured']
        injured = request.form['injured']
        damage_status = request.form['damage_status']
        aid_type = request.form['aid_type']
        aid_amount = request.form.get('aid_amount', '').strip()
        area = request.form['area']
        landmark = request.form['landmark']
        gender = request.form['gender']
        marital_status = request.form['marital_status']
        wives_count = request.form['wives_count']
        wife2_name = request.form['wife2_name']
        wife2_national_id = request.form['wife2_national_id']
        wife3_name = request.form['wife3_name']
        wife3_national_id = request.form['wife3_national_id']
        wife4_name = request.form['wife4_name']
        wife4_national_id = request.form['wife4_national_id']
        Resident_displaced = request.form['Resident_displaced']
        notes = request.form['notes']
        other_type_help = request.form['other_type_help']

        # معالجة aid_amount حسب نوع المساعدة
        if aid_type == 'قيمة مالية':
            try:
                aid_amount = float(aid_amount)
            except (ValueError, TypeError):
                aid_amount = 0
        else:
            aid_amount = None

        # إذا الحالة الاجتماعية أعزب، احذف بيانات الزوجة والزوجات
        if marital_status == "أعزب":
            name_female = None
            national_id_2 = None
            wives_count = None
            wife2_name = None
            wife2_national_id = None
            wife3_name = None
            wife3_national_id = None
            wife4_name = None
            wife4_national_id = None

        cursor.execute("""
            UPDATE beneficiaries SET 
                name_male=%s, name_female=%s, national_id_1=%s, national_id_2=%s, phone_number=%s,
                family_members=%s, family_members_injured=%s, injured=%s, damage_status=%s,
                aid_type=%s, aid_amount=%s, area=%s, landmark=%s, gender=%s, marital_status=%s,
                wives_count=%s, wife2_name=%s, wife2_national_id=%s, wife3_name=%s, wife3_national_id=%s,
                wife4_name=%s, wife4_national_id=%s, notes=%s, other_type_help=%s, Resident_displaced=%s
            WHERE national_id_1=%s
        """, (
            name_male, name_female, national_id_1, national_id_2, phone_number,
            family_members, family_members_injured, injured, damage_status,
            aid_type, aid_amount, area, landmark, gender, marital_status,
            wives_count, wife2_name, wife2_national_id, wife3_name, wife3_national_id,
            wife4_name, wife4_national_id, notes, other_type_help, Resident_displaced, national_id
        ))

        db.commit()
        cursor.close()
        save_notification(f"تمت تعديل بيانات مستفيد: {national_id}")
        return redirect(url_for('dashboard'))

    # GET: عرض النموذج بالبيانات القديمة
    cursor.execute("SELECT * FROM beneficiaries WHERE national_id_1 = %s", (national_id,))
    beneficiary = cursor.fetchone()
    cursor.close()
    return render_template('edit.html', record=beneficiary)



# حذف مستفيد
@app.route('/delete/<national_id_1>', methods=['POST'])
def delete(national_id_1):
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    cursor.execute("SELECT name_male FROM beneficiaries WHERE national_id_1 = %s", (national_id_1,))
    name = cursor.fetchone()
    
    if not name:
        return jsonify({'error': 'Record not found'}), 404
    
    try:
        cursor.execute("DELETE FROM beneficiaries WHERE national_id_1 = %s", (national_id_1,))
        db.commit()
        save_notification(f"تم حذف المستفيد: {name['name_male']}")
        return jsonify({'success': True}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/donate', methods=['GET', 'POST'])
def donate():
    # تحقق إذا كان المستخدم أدمن، إذا لا فارجعه للصفحة الرئيسية
    if session.get('role') != 'admin':
        return redirect(url_for('dashboard'))  # أو أي صفحة رئيسية

    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        donor_name = request.form.get('donor_name') or 'لا يوجد'
        contact = request.form.get('contact') or 'لا يوجد'
        aid_type = request.form.get('aid_type') or 'لا يوجد'

        # تأكد أن amount رقم، أو اجعله NULL في حال لم يكن رقمًا
        raw_amount = request.form.get('amount')
        try:
            amount = float(raw_amount)
        except (TypeError, ValueError):
            amount = None  # أو 0.0 إذا أردت قيمة افتراضية

        description = request.form.get('description') or 'لا يوجد'
        beneficiary_national_id = request.form.get('beneficiary_national_id') or None
        status = request.form.get('status') or 'لم يتم'

        try:
            cursor.execute("""
                INSERT INTO donations (
                    donor_name, contact, aid_type, amount, description,
                    beneficiary_national_id, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                donor_name, contact, aid_type, amount, description,
                beneficiary_national_id, status
            ))
            db.commit()
            save_notification(f"تم تسجيل مساعدة جديدة من {donor_name}")
            return redirect(url_for('dashboard'))

        except Exception as e:
            db.rollback()
            return f"حدث خطأ: {str(e)}", 500

        finally:
            cursor.close()

    return render_template('donate.html')


@app.route('/donations')
def donations():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('dashboard'))  # أو أي صفحة رئيسية عندك

    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, donor_name, contact, aid_type, status, created_at 
        FROM donations 
        ORDER BY created_at DESC
    """)
    donations = cursor.fetchall()
    cursor.close()
    return render_template('donations.html', donations=donations)


@app.route('/donation_details/<int:id>')
def donation_details(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    cursor = db.cursor()
    cursor.execute("SELECT * FROM donations WHERE id = %s", (id,))
    row = cursor.fetchone()

    if not row:
        return "المتبرع غير موجود", 404

    columns = [desc[0] for desc in cursor.description]
    donation = dict(zip(columns, row))

    cursor.close()

    return render_template('donation_details.html', donation=donation)





@app.route('/delete_donor/<int:id>', methods=['POST'])
def delete_donor(id):
    print("استقبال طلب حذف للمعرف:", id)

    if 'user' not in session:
        print("المستخدم غير مسجل دخول")
        return jsonify({'error': 'Unauthorized'}), 401

    cursor.execute("SELECT donor_name FROM donations WHERE id = %s", (id,))
    donor = cursor.fetchone()
    print("المتبرع:", donor)

    if not donor:
        return jsonify({'error': 'Record not found'}), 404

    try:
        donor_name = donor['donor_name'] if isinstance(donor, dict) else donor[0]
        cursor.execute("DELETE FROM donations WHERE id = %s", (id,))
        db.commit()
        save_notification(f"تم حذف المتبرع: {donor_name}")
        return jsonify({'success': True}), 200
    except Exception as e:
        print("خطأ:", str(e))
        db.rollback()
        return jsonify({'error': str(e)}), 500


# عرض تفاصيل
@app.route('/details/<national_id_1>')
def details(national_id_1):
    if 'user' not in session:
        return redirect(url_for('login'))

    # استعلام إحضار كل الأعمدة
    cursor.execute("SELECT * FROM beneficiaries WHERE national_id_1 = %s", (national_id_1,))
    
    person = cursor.fetchone()

    if not person:
        return "المستفيد غير موجود", 404

    # استخراج أسماء الأعمدة تلقائيًا من الوصف
    columns = [desc[0] for desc in cursor.description]
    
    # تحويل النتائج إلى dict
    person_dict = dict(zip(columns, person))

    return render_template('details.html', person=person)





# عرض الإشعارات
@app.route('/notifications')
def notifications():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notifications ORDER BY created_at DESC LIMIT 10")
    rows = cursor.fetchall()
    cursor.close()

    notifications = []
    for row in rows:
        notif = dict(row)  # row بالفعل dict إذا استخدمت dictionary=True

        created_at = notif.get('created_at')
        if isinstance(created_at, datetime):
            notif['created_at'] = created_at.strftime('%Y-%m-%d ')
        elif created_at is None:
            notif['created_at'] = ''
        else:
            notif['created_at'] = str(created_at)

        notifications.append(notif)

    return jsonify(notifications)

# صفحة التحليل
@app.route('/analytics')
def analytics():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('dashboard'))
    # 1- إجمالي عدد المستفيدين
    cursor.execute("SELECT COUNT(*) as total FROM beneficiaries")
    total = cursor.fetchone()['total']

    # 2- عدد المصابين
    cursor.execute("SELECT COUNT(*) as injured FROM beneficiaries WHERE injured = 'نعم'")
    injured = cursor.fetchone()['injured']

    # 3- عدد المتضررين كلياً
    cursor.execute("SELECT COUNT(*) as fully_damaged FROM beneficiaries WHERE damage_status = 'كلي'")
    fully_damaged = cursor.fetchone()['fully_damaged']

    # 4- عدد المقيمين
    cursor.execute("SELECT COUNT(*) as residents FROM beneficiaries WHERE Resident_displaced = 'مقيم'")
    residents = cursor.fetchone()['residents']

    # 5- عدد النازحين
    cursor.execute("SELECT COUNT(*) as displaced FROM beneficiaries WHERE Resident_displaced = 'نازح'")
    displaced = cursor.fetchone()['displaced']

    # 6- عدد المستفيدين حسب نوع المساعدة
    cursor.execute("SELECT aid_type, COUNT(*) as count FROM beneficiaries GROUP BY aid_type")
    aid_data = cursor.fetchall()
    aid_labels = [row['aid_type'] for row in aid_data]
    aid_counts = [row['count'] for row in aid_data]

    # 7- نسبة الذكور والإناث
    cursor.execute("SELECT Resident_displaced, COUNT(*) as count FROM beneficiaries GROUP BY Resident_displaced")
    status_data = cursor.fetchall()

    status_labels = [row['Resident_displaced'] for row in status_data]
    status_counts = [row['count'] for row in status_data]


    # 8- عدد المتضررين حسب نوع الضرر
    cursor.execute("SELECT damage_status, COUNT(*) as count FROM beneficiaries GROUP BY damage_status")
    damage_data = cursor.fetchall()
    damage_labels = [row['damage_status'] for row in damage_data]
    damage_counts = [row['count'] for row in damage_data]

    return render_template("analytics.html",
                           total=total,
                           injured=injured,
                           fully_damaged=fully_damaged,
                           residents=residents,
                           displaced=displaced,
                           aid_labels=aid_labels,
                           aid_counts=aid_counts,
                           status_labels=status_labels,
                           status_counts=status_counts,
                           damage_labels=damage_labels,
                           damage_counts=damage_counts)


# تسجيل الإشعارات
def save_notification(message):
    cursor.execute("INSERT INTO notifications (message, created_at) VALUES (%s, %s)", (message, datetime.now()))
    db.commit()





# تسجيل الخروج
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
