$(document).ready(function() {

    $("#addCancelBtn").click(function(){
        $("#addRow").hide();
    });

    $("#editCancelBtn").click(function(){
        $("#editRow").hide();
    });

});

function onRowClick(td_array) {
    var a = JSON.parse(td_array);
    fillEditInputs(a);
    console.log(JSON.stringify(a));
    showEdit();
}

function onAddClick() {
    showAdd();
}

function fillEditInputs(obj){
    $("#id_editId").val(obj.id);
    $("#id_editFrom").val(obj.from_id);
    $("#id_editTo").val(obj.to_id);
    $("#id_editPlayer").val(obj.player_id);
    $("#id_editPrice").val(obj.price);
    $("#id_editDate").val(obj.date);
}

function showEdit() {
    $("#addRow").hide();
    $("#editRow").show();
}

function showAdd() {
    $("#editRow").hide();
    $("#addRow").show();
}




