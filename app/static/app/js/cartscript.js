var updateBtns = document.getElementsByClassName('update-cart')


 for ( i=0; i< updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        
        console.log('productId:', productId, 'action:', action)
        console.log('USER',user)
    
         
        if(user=='AnonymousUser'){
            alert('please login First! You are' + user + 'User')
        } 
        else{
         updateUserOrder(productId, action)
         console.log(productId, action)
          // console.log('User logged in,sending data')
        }
    })
 }
 function updateUserOrder(productId, action){
  console.log('user is logged in , sending data..')

  var url= '/add-to-cart/'

  fetch(url, {
    method:'POST',
    headers:{
      'Content-Type':'application/json',
       'X-CSRFToken':csrftoken,

    },
    body: JSON.stringify({'productId': productId,'action':action})
  })
  .then((response)=>{
    return response.json()
  })
   .then((data)=>{
      console.log('data:',data)
      location.reload()
   })  
  }
   
$('.minus-cart').click(function(){
   var id=  this.dataset.product
   var eml = this.parentNode.children[2]
   console.log(id)
   $.ajax(
    {
      type:"GET",
      url: "/minuscart",
      data:{
          prod_id: id
      },
      success:function (data){
        console.log(data)
         eml.innerText = data.quantity
         document.getElementById("carttotal").innerText=data.carttotal
         document.getElementById("total").innerText=data.amount
         document.getElementById("producttotal").innerText=data.carttotal
      }
    }
   )
})
$('.remove-cart').click(function(){
  var id=  this.dataset.product
  var eml = this 
  console.log(id)
  $.ajax(
   {
     type:"GET",
     url: "/removecart",
     data:{
         prod_id: id
     },
     success:function (data){
       console.log(data)
        
        document.getElementById("carttotal").innerText=data.carttotal
        document.getElementById("total").innerText=data.amount
        document.getElementById("producttotal").innerText=data.carttotal
        eml.parentNode.parentNode.parentNode.parentNode.remove()
        
     }
   }
  )
})