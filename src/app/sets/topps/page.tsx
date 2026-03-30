import { redirect } from "next/navigation";

export default function ToppsRedirect() {
  redirect("/sets?manufacturer=Topps");
}
