import React from "react";
import IndivScore from "./indiv-metric";

const Summary = () => {
  return (
    <>
      <div className="w-full h-full flex space-x-8">
        <div className="flex-2 h-full grid grid-rows-6 ">
          <div className="row-span-1 grid grid-cols-6 ">
            <div className="col-span-5 b flex space-x-8 items-center px-6">
              <h1 className="text-gray-600 text-4xl font-bold">#91</h1>
              <h1 className="font-semibold text-3xl ">John Doe</h1>
            </div>
          </div>
          <div className="row-span-5">
            <p className="text-slate-400">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Doloribus
              soluta incidunt cupiditate cumque. Fugit numquam rerum facilis
              quae dolorem? Perferendis atque molestiae nihil debitis ut
              adipisci mollitia aliquid. Necessitatibus, harum. Lorem ipsum
              dolor sit amet consectetur adipisicing elit. Earum hic, quae
              maiores aspernatur consequuntur explicabo maxime ad eum dolor amet
              numquam molestias sequi libero quod at repellendus vel? Veritatis,
              perferendis! Lorem ipsum dolor sit amet consectetur adipisicing
              elit. <br /> <br />
              Molestiae laboriosam officia iste numquam distinctio nulla
              doloremque nemo inventore quia excepturi nam aliquam sapiente
              incidunt autem, vel amet facere cumque fugiat! Lorem ipsum dolor
              sit amet consectetur adipisicing elit. Dolores atque sit pariatur
              error necessitatibus ab! Quis, sit dicta quae adipisci a vitae non
              soluta porro, sunt ipsam, laborum pariatur labore? Lorem ipsum
              dolor sit amet, consectetur adipisicing elit. Natus, illo,
              cupiditate voluptate, dolores minus eum quo eveniet alias
              laboriosam cumque doloremque et assumenda consequuntur repellendus
              voluptatibus beatae nobis ducimus quidem!
            </p>
          </div>
        </div>
        <div className="h-full flex-1 grid grid-row-6">
          <h1 className="text-white text-4xl font-bold row-span-1 content-center justify-self-end">
            9/10
          </h1>
          <div className="row-span-5">
            <IndivScore />
          </div>
        </div>
      </div>
    </>
  );
};

export default Summary;
