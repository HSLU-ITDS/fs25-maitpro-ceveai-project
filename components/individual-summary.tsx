import React from "react";
import IndivScore from "./indiv-metric";

const Summary = () => {
  return (
    <>
      <div className="w-full h-full flex space-x-8">
        <div className="flex-2 h-full flex flex-col ">
          <div className="grid grid-cols-6">
            <div className="col-span-5 flex space-x-8 px-6 pb-4">
              <h1 className="text-gray-600 text-4xl font-bold">#91</h1>
              <h1 className="font-semibold text-3xl">John Doe</h1>
            </div>
          </div>
          <div className="flex-1 overflow-auto px-6">
            <p className="text-muted-foreground text-sm">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Doloribus
              soluta incidunt cupiditate cumque. Fugit numquam rerum facilis
              quae dolorem? Perferendis atque molestiae nihil debitis ut
              adipisci mollitia aliquid. Necessitatibus, harum. Lorem ipsum
              dolor sit amet consectetur adipisicing elit. Earum hic, quae
              maiores aspernatur consequuntur explicabo maxime ad eum dolor amet
              numquam molestias sequi libero quod at repellendus vel? Veritatis,
              perferendis! <br /> <br />
              Molestiae laboriosam officia iste numquam distinctio nulla
              doloremque nemo inventore quia excepturi nam aliquam sapiente
              incidunt autem, vel amet facere cumque fugiat! Lorem ipsum dolor
              sit amet consectetur adipisicing elit. Dolores atque sit pariatur
              error necessitatibus ab! Quis, sit dicta quae adipisci a vitae non
              soluta porro, sunt ipsam, laborum pariatur labore? Lorem ipsum
              dolor sit amet, consectetur adipisicing elit.
            </p>
          </div>
        </div>
        <div className="h-full flex-1 grid grid-row-6">
          <h1 className="text-primary text-4xl font-bold row-span-1 justify-self-end">
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
