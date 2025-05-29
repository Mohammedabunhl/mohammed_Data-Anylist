$(document).ready(function () {
      const table = $('#beneficiariesTable').DataTable({
        dom: 'Bfrtip',
        buttons: [
          {
            extend: 'excelHtml5',
            text: '📥 تصدير إلى Excel',
            className: 'exportExcel',
            exportOptions: {
              columns: ':not(:last-child)',
              format: {
                header: function (data, columnIdx) {
                  const columnNames = ['الاسم رباعي', 'رقم الهوية', 'رقم الجوال', 'عدد الأفراد', 'نوع المساعدة', 'تاريخ التسليم'];
                  return columnNames[columnIdx] || data;
                }
              }
            }
          }
        ],
        language: {
          url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/ar.json'
        },
        pageLength: 100,
        lengthChange: false,
        searching: true,
        columnDefs: [
          { targets: -1, orderable: false }
        ]
      });

      // زر حذف السطر - فقط للأدمن
      $('#beneficiariesTable tbody').on('click', 'button.delete-btn', function () {
        if (confirm('هل أنت متأكد من حذف هذا المستفيد؟')) {
          const row = $(this).closest('tr');
          const nationalId = row.attr('data-id');
          $.ajax({
            url: `/delete/${nationalId}`,
            type: 'POST',
            success: function (response) {
              if (response.success) {
                table.row(row).remove().draw();
              } else {
                alert('حدث خطأ أثناء الحذف');
              }
            },
            error: function () {
              alert('فشل الاتصال بالخادم');
            }
          });
        }
      });

      // إشعارات - افتح وأغلق القائمة
      $('#notificationIcon').on('click keydown', function (e) {
  // إذا الحدث من لوحة المفاتيح غير Enter أو Space، نتركه
  if (e.type === 'keydown' && e.key !== 'Enter' && e.key !== ' ') {
    return;
  }

  // إذا الضغط على رابط داخل القائمة نتركه يشتغل عادي
  if ($(e.target).closest('#notifDropdown a').length > 0) {
    return;
  }

  e.preventDefault();
  $(this).toggleClass('active');
  const expanded = $(this).attr('aria-expanded') === 'true';
  $(this).attr('aria-expanded', !expanded);
});

// إغلاق الإشعارات عند الضغط خارجها
$(document).on('click', function (e) {
  if (!$(e.target).closest('#notificationIcon').length) {
    $('#notificationIcon').removeClass('active').attr('aria-expanded', 'false');
  }
});


      // إغلاق الإشعارات عند الضغط خارجها
      $(document).on('click', function (e) {
        if (!$(e.target).closest('#notificationIcon').length) {
          $('#notificationIcon').removeClass('active').attr('aria-expanded', 'false');
        }
      });
    });



