import { Navbar } from "@/components/Navbar";
import { Recommend } from "@/components/Recommend";
import { useRouter } from "next/router";
import { useState } from "react";

export default function Recomd(){
    const router=useRouter();
    const [data, setData]=useState([]);
    const userId=router.query.userId;
    useEffect(()=>{
        if(router.isReady){
          fetch(`write get request`,{
            method:"GET"
          }).then((res)=>
            res.json()
          ).then((data)=>{
            setData(data);
          })
        }
        },[router.isReady])
        // send array 
    return(
        <div>
            <Navbar/>
            <Recommend array={data}/> 
        </div>
    )
}