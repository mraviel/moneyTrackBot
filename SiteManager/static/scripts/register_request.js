
function remove_request(li_id){
    console.log(li_id)
    const li = document.querySelector(`#${li_id}`)
    li.remove()
    
}

function accept_register(li_id){
    // Do Some things
    console.log("accepted")
    remove_request(li_id)
}