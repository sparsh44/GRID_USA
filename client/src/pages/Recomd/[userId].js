import { Navbar } from "@/components/Navbar";
import { Recommend } from "@/components/Recommend";
import { useRouter } from "next/router";
import { useState , useEffect} from "react";
import axios from 'axios';

export default function Recomd(){
    const router=useRouter();
    const [dataArr, setDataArr]=useState([]);
    const userId=router.query.userId;
    useEffect(()=>{
        if(router.isReady){
            const response = axios.post('http://127.0.0.1:5000/', {
              data:userId,
              headers: {
                'Access-Control-Allow-Origin' : '*',
              }
            }).then((res) => {
              console.log(res)
              setDataArr(res.data)
            });
          }
        },[router.isReady])
        // send array 
    return(
        <div>
            <Navbar/>
            {dataArr?(<Recommend array={dataArr}/>):(<div>Loading</div>)} 
        </div>
    )
}