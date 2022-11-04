
function remove_request(btn_id){
    let register_id = btn_id.split('-')[2]
    let li_id = `li-${register_id}`
    
    // Remove li from window
    const li = document.querySelector(`#${li_id}`)
    li.remove()
}