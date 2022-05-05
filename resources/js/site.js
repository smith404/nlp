if (typeof define === "function" && define.amd) {
  define(["jquery"]);
} else if (typeof exports === "object") {
  if (typeof $ === "undefined") {
    module.exports = require("jquery");
  } else {
    module.exports = $;
  }
}

let modalTemplate = {
  dialog:
    '<div id="boot4alert" class="modal fade">' +
    '<div class="modal-dialog">' +
    '<div class="modal-content">' +
    '<div class="modal-body"></div>' +
    '</div>' +
    '</div>' +
    '</div>',
  header:
    '<div class="modal-header">' + '<h5 class="modal-title"></h5>' + "</div>",
  footer: '<div class="modal-footer"></div>',
  closeButton:
    '<button class="close" style="margin-top: -15px;"  data-dismiss="modal">' +
    '<span>&times;</span>' +
    '</button>',
  button:
    '<button class="btn btn-primary boot4ok" data-dismiss="modal" type="button"></button>',
  buttonConfirm:
    '<button class="btn btn-secondary boot4cancel" data-dismiss="modal" type="button">Cancel</button>' +
    '<button class="btn btn-primary boot4ok" data-dismiss="modal" type="button">OK</button>'
};

let dialog = $(modalTemplate.dialog);
let body = dialog.find(".modal-body");
let callbacks = { onEscape: "" };

function Initial(msg, btnMsg) {
  let tmsg = "";

  if ((msg.callback != undefined || msg.confirm) && !$.isFunction(msg.callback)) {
    throw new Error("Alert requires callback property to be a function");
  }

  if (msg.msg != undefined) {
    tmsg = msg.msg;
  }
  else if (msg.title != undefined) {
    tmsg = msg.msg;
  }
  else {
    tmsg = msg + modalTemplate.closeButton;
  }

  if (msg.title != undefined && dialog.find(".modal-header").length == 0) {
    body.before(modalTemplate.header);
    dialog.find(".modal-header").html(msg.title + modalTemplate.closeButton);
  }

  if (msg.style != undefined) {
    dialog.find(".modal-header").css(msg.style);
  }

  if (dialog.find(".btn-primary").length == 0) {
    body.after(modalTemplate.footer);
    if (msg.confirmBox != undefined) {
      dialog.find(".modal-footer").html(modalTemplate.buttonConfirm);
    } else {
      dialog.find(".modal-footer").html(modalTemplate.button);
      dialog.find(".btn").html(btnMsg);
    }
  }
  dialog.find(".modal-body").html(tmsg);
  if (msg.size != undefined) {
    switch (msg.size) {
      case "sm":
        dialog.find(".modal-dialog").addClass("modal-sm");
        break;
      case "lg":
        dialog.find(".modal-dialog").addClass("modal-lg");
        break;
      case "xl":
        dialog.find(".modal-dialog").addClass("modal-xl");
        break;
      default:
        break;
    }
  }
}

let boot4 = {
  alert: function (msg, btnMsg, options) {
    Initial(msg, btnMsg);
    $("body").append(dialog);
    if (msg.callback != undefined) {
      $("#boot4alert").modal(options);
      return (callbacks.onEscape = msg.callback);
    } else {
      return $("#boot4alert").modal(options);
    }
  },
  confirm: function (msg, options) {
    msg.confirmBox = true;
    Initial(msg);
    $("body").append(dialog);
    $("#boot4alert").modal(options);
    return (callbacks.onEscape = msg.callback);
  }
};

function processCallback(e, dialog, callback, result) {
  e.stopPropagation();
  e.preventDefault();
  let preserveDialog =
    $.isFunction(callback) && callback.call(dialog, result, e) === false;
  if (!preserveDialog) {
    dialog.modal("hide");
  }
}

dialog.on("click", ".boot4ok", function (e) {
  processCallback(e, dialog, callbacks.onEscape, true);
});
dialog.on("click", ".boot4cancel", function (e) {
  processCallback(e, dialog, callbacks.onEscape, false);
});

var waitingDialog = waitingDialog || (function ($) {
  'use strict';
  let $dialog = $(
    '<div class="modal fade" data-backdrop="static" data-keyboard="false" tabindex="-1" role="dialog" aria-hidden="true" style="padding-top:15%; overflow-y:visible;">' +
    '<div class="modal-dialog modal-m">' +
    '<div class="modal-content">' +
    '<div class="modal-header"><h3 style="margin:0;"></h3></div>' +
    '<div class="modal-body">' +
    '<div class="progress progress-striped active" style="margin-bottom:0;"><div class="progress-bar" style="width: 100%"></div></div>' +
    '</div>' +
    '</div></div></div>');

  return {
    show: function (message, options) {
      // Defaults
      if (typeof options === 'undefined') {
        options = {};
      }
      if (typeof message === 'undefined') {
        message = 'Loading';
      }
      let settings = $.extend({
        dialogSize: 'm',
        progressType: '',
        onHide: null
      }, options);

      // Configuring the dialog
      $dialog.find('.modal-dialog').attr('class', 'modal-dialog').addClass('modal-' + settings.dialogSize);
      $dialog.find('.progress-bar').attr('class', 'progress-bar');

      if (settings.progressType) {
        $dialog.find('.progress-bar').addClass('progress-bar-' + settings.progressType);
      }
      $dialog.find('h3').text(message);

      if (typeof settings.onHide === 'function') {
        $dialog.off('hidden.bs.modal').on('hidden.bs.modal', function (e) {
          settings.onHide.call($dialog);
        });
      }

      // Open the dialog
      $dialog.modal();
    },

    hide: function () {
      // Close the dialog
      $dialog.modal('hide');
    }
  };
})(jQuery);

const toSingleLine = (theText) => {
  return theText.replace(/[\n\r]/g, '');
};

const toAlphNumeric = (theText) => {
  return theText.replace(/[^a-z0-9]/gi, '');
};

const toCamelCase = (theText) => {
  return theText.str.replace(/(?:^\w|[A-Z]|\b\w)/g, function (word, index) {
    return index === 0 ? word.toLowerCase() : word.toUpperCase();
  }).replace(/\s+/g, '');
};

const toSnakeCase = (theText) => {
  return theText.replace(/\.?([A-Z])/g, function (x, y) { return "_" + y.toLowerCase() }).replace(/^_/, "");
};

const toTitleCase = (theText) => {
  return theText
    .toLowerCase()
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

function camelize(str) {
  return str.replace(/(?:^\w|[A-Z]|\b\w)/g, function (word, index) {
    return index === 0 ? word.toLowerCase() : word.toUpperCase();
  }).replace(/\s+/g, '');
}

function fakeDownload(filename, text) {
  let element = document.createElement('a');

  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);
  element.style.display = 'none';

  document.body.appendChild(element);
  element.click();

  document.body.removeChild(element);
}

function makeButtonList(entities, container, callback) {
  // List container
  let listContainer = document.getElementById(container);
  let entity;
  for (entity of entities) {
    let b = document.createElement('button');
    b.className = 'list-group-item list-group-item-action';
    b.type = 'button';
    b.innerHTML = entity.name;
    b.setAttribute('ng-click', callback + '(' + entity.id + ')');

    listContainer.appendChild(b);
  }
};

function makeNamedEntityTable(entities, container, fields) {
  // Table container
  let tableContainer = document.getElementById(container);

  tableCreate(entities, tableContainer, fields);
};

function searchAndReplace(target, fields, entity) {
  let field;
  let res = target;
  for (field of fields) {
    res = res.replace('@' + field.name, entity[field.name]);
  }

  return res;
};

function isEmpty(obj) {
  for (let prop in obj) {
    if (obj.hasOwnProperty(prop)) return false;
  }
  return true;
};

function showSuccess(response) {
  waitingDialog.show('Saved successfully...', { dialogSize: 'sm', progressType: 'striped bg-success progress-bar-animated' });
  setTimeout(function () { waitingDialog.hide(); }, 3000);
};

function showFailure(response) {
  exceptionAlert('An Error has Occurred', response.data.details);
};

function exceptionAlert(title, message) {
  boot4.alert({ msg: message, title: title }, "Continue");
};

function toSingleTrimmedLine(rawText) {
  rawText = rawText.replace(/\n/g, ' ');
  rawText = rawText.replace(/\s\s+/g, ' ');
  rawText = rawText.trim();

  return rawText
}

function uuidv4() {
  return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  );
}


