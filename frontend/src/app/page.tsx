import { redirect } from "next/navigation";

// export const metadata: Metadata = {
//   title: "Recapify - Get Legal Help in Your Language",
//   description: "Access Youtube assistance in your language with Recapify.",
// };

const Page = () => {
  redirect("/login");
  // return <LandingPage />;
};

export default Page;
