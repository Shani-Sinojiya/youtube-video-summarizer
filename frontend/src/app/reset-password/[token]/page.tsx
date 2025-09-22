import Logo from "@/components/logo";
import { ResetPasswordForm } from "@/components/reset-password-form";
import { WEB_APP_BASENAME } from "@/constants/web";
import { Metadata } from "next";
import Link from "next/link";

export const dynamic = "force-dynamic";
export const revalidate = 0;
export const fetchCache = "force-no-store";
export const runtime = "edge";

const TokenVerification = async (token: string): Promise<boolean> => {
  const url = `${process.env.NEXT_PUBLIC_API_URL}/api/auth/reset-password/verify`;

  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ hash: token }),
  });

  if (!response.ok) {
    throw new Error("Invalid or expired reset token");
  }

  return true;
};

export default async function ResetPasswordPage({
  params,
}: {
  params: Promise<{ token: string }>;
}) {
  const { token } = await params;

  if (!token) {
    return (
      <div className="bg-muted flex min-h-svh flex-col items-center justify-center gap-6 p-6 md:p-10">
        <div className="flex w-full max-w-sm flex-col gap-6">
          <Link
            href="/"
            className="flex items-center gap-2 self-center font-medium"
          >
            <div className="bg-primary text-primary-foreground flex size-6 items-center justify-center rounded-md">
              <Logo className="h-4 w-4" />
            </div>
            {WEB_APP_BASENAME}
          </Link>
          <div className="text-center text-red-500">
            Invalid or missing reset token. Please try again.
          </div>
        </div>
      </div>
    );
  }

  try {
    await TokenVerification(token);
  } catch (error) {
    return (
      <div className="bg-muted flex min-h-svh flex-col items-center justify-center gap-6 p-6 md:p-10">
        <div className="flex w-full max-w-sm flex-col gap-6">
          <Link
            href="/"
            className="flex items-center gap-2 self-center font-medium"
          >
            <div className="bg-primary text-primary-foreground flex size-6 items-center justify-center rounded-md">
              <Logo className="h-4 w-4" />
            </div>
            {WEB_APP_BASENAME}
          </Link>
          <div className="text-center text-red-500">
            {error instanceof Error ? error.message : "An error occurred."}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-muted flex min-h-svh flex-col items-center justify-center gap-6 p-6 md:p-10">
      <div className="flex w-full max-w-sm flex-col gap-6">
        <Link
          href="/"
          className="flex items-center gap-2 self-center font-medium"
        >
          <div className="bg-primary text-primary-foreground flex size-6 items-center justify-center rounded-md">
            <Logo className="h-4 w-4" />
          </div>
          {WEB_APP_BASENAME}
        </Link>
        <ResetPasswordForm />
      </div>
    </div>
  );
}

export const metadata: Metadata = {
  title: "Reset Password | " + WEB_APP_BASENAME,
  description: "Reset your password to access the application.",
};
