import React from "react";
import UI from "./ui";
import { auth } from "@/auth";
import { redirect } from "next/navigation";

const Page = async () => {
  const session = await auth();

  if (!session) {
    redirect("/login");
  }

  return <UI />;
};

export default Page;
