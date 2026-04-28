// (() => {
//     var c = document.querySelector("#flatpickr-range-create");
//     var u = document.querySelector("#flatpickr-range-update");
//     var d = document.querySelector("#flatpickr-range-delete");
//     null != typeof c && c.flatpickr({mode: "range", static: !0}),
//     u && u.flatpickr({mode: "range", static: !0}),
//     d && d.flatpickr({mode: "range", static: !0})

// dropzone needsclick

// })();
const testtesttest = (e, target_id) => {
    // $(`#${target_id}`).click();
    new Dropzone(e, {
        previewTemplate: `<div class="dz-preview dz-file-preview">
<div class="dz-details">
  <div class="dz-thumbnail">
    <img data-dz-thumbnail>
    <span class="dz-nopreview">No preview</span>
    <div class="dz-success-mark"></div>
    <div class="dz-error-mark"></div>
    <div class="dz-error-message"><span data-dz-errormessage></span></div>
    <div class="progress">
      <div class="progress-bar progress-bar-primary" role="progressbar" aria-valuemin="0" aria-valuemax="100" data-dz-uploadprogress></div>
    </div>
  </div>
  <div class="dz-filename" data-dz-name></div>
  <div class="dz-size" data-dz-size></div>
</div>
</div>`, parallelUploads: 1, maxFilesize: 5, acceptedFiles: ".jpg,.jpeg,.png,.gif", addRemoveLinks: !0, maxFiles: 1
    });
};