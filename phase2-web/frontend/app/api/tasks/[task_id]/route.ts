import { auth } from "@/app/lib/auth"
import { NextRequest, NextResponse } from "next/server"
import crypto from "node:crypto"

export const runtime = "nodejs"

function requireEnv(name: string): string {
  const value = process.env[name]
  if (!value) throw new Error(`Missing env var: ${name}`)
  return value
}

function signInternalRequest(args: {
  userId: string
  timestamp: string
  method: string
  path: string
  body: string
}) {
  const secret = requireEnv("BETTER_AUTH_SECRET")
  const payload = `${args.userId}:${args.timestamp}:${args.method}:${args.path}:${args.body}`

  const signature = crypto
    .createHmac("sha256", secret)
    .update(payload)
    .digest("hex")

  return { signature, payload }
}

async function requireUserId(request: Request): Promise<string> {
  const session = await auth.api.getSession({ headers: request.headers })
  if (!session?.user?.id) {
    throw new Response(JSON.stringify({ detail: "Unauthorized" }), {
      status: 401,
      headers: { "content-type": "application/json" },
    })
  }
  return session.user.id
}

async function proxyToBackend(request: Request, opts: { method: string; path: string; body?: string }) {
  const backendBase = requireEnv("NEXT_PUBLIC_API_URL")
  const userId = await requireUserId(request)
  const timestamp = Date.now().toString()
  const body = opts.body ?? ""

  const { signature } = signInternalRequest({
    userId,
    timestamp,
    method: opts.method,
    path: opts.path,
    body,
  })

  const res = await fetch(`${backendBase}${opts.path}`, {
    method: opts.method,
    headers: {
      "content-type": "application/json",
      "x-user-id": userId,
      "x-internal-timestamp": timestamp,
      "x-internal-signature": signature,
    },
    body: opts.method === "GET" || opts.method === "DELETE" ? undefined : body,
  })

  if (res.status === 204) {
    return new NextResponse(null, { status: 204 })
  }

  const text = await res.text()
  const contentType = res.headers.get("content-type") || "application/json"
  return new NextResponse(text, {
    status: res.status,
    headers: { "content-type": contentType },
  })
}

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ task_id: string }> }
) {
  try {
    const { task_id } = await params
    return await proxyToBackend(request, {
      method: "GET",
      path: `/api/tasks/${task_id}`,
    })
  } catch (err) {
    if (err instanceof Response) return err
    return NextResponse.json({ detail: "Internal server error" }, { status: 500 })
  }
}

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ task_id: string }> }
) {
  try {
    const { task_id } = await params
    const body = await request.text()
    return await proxyToBackend(request, {
      method: "PUT",
      path: `/api/tasks/${task_id}`,
      body,
    })
  } catch (err) {
    if (err instanceof Response) return err
    return NextResponse.json({ detail: "Internal server error" }, { status: 500 })
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ task_id: string }> }
) {
  try {
    const { task_id } = await params
    return await proxyToBackend(request, {
      method: "DELETE",
      path: `/api/tasks/${task_id}`,
    })
  } catch (err) {
    if (err instanceof Response) return err
    return NextResponse.json({ detail: "Internal server error" }, { status: 500 })
  }
}
