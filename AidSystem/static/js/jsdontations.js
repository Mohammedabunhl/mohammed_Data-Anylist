$(document).ready(function () {
    const table = $('#donationTable').DataTable({
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.4/i18n/ar.json'
        }
    });

    // حذف المتبرع عند الضغط على الزر
    $('#donationTable').on('click', '.delete', function (e) {
        e.preventDefault();
        const row = $(this).closest('tr');
        const id = $(this).data('id');

        if (!id) {
            alert('معرف المتبرع غير موجود');
            return;
        }

        if (confirm('هل أنت متأكد من الحذف؟')) {
            fetch(`/delete_donor/${id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    table.row(row).remove().draw();
                    console.log("تم الحذف بنجاح");
                } else {
                    alert('فشل في الحذف: ' + (data.error || 'غير معروف'));
                }
            })
            .catch(err => {
                alert('حدث خطأ أثناء الحذف');
                console.error(err);
            });
        }
    });
});
