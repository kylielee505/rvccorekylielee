import { client } from "@gradio/client";
import type { NextApiRequest, NextApiResponse } from "next";
import fs from "fs";
import path from "path";

type Data = { data: any };

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  const body = JSON.parse(req.body);
  if (body.file) {
    const result = await demucs(body.file);
    res.status(200).json({ data: result });
  } else {
    const result = await musicgen(body);
    res.status(200).json({ data: result });
  }
}

// demucs handler
export async function demucsHandler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  const body = JSON.parse(req.body);
  const result = await demucs(body.file);
  res.status(200).json({ data: result });
}

async function demucs(file: string) {
  const audioBlob = await getFile(file);

  const app = await client("http://127.0.0.1:7865/");
  const result = await app.predict("/demucs", [
    audioBlob, // blob in 'Input' Audio component
  ]);

  return result?.data;
}

const readFromDisk = (file: string) =>
  new Promise((resolve, reject) => {
    fs.readFile(
      path.join(process.cwd(), "public", file),
      (err, data) => {
        if (err) reject(err);
        resolve(data);
      }
    );
  });

const readFromURL = (file: string) => fetch(file).then((r) => r.blob());

const getFile = (file: string) =>
  file
    ? file.startsWith("http") || file.startsWith("data")
      ? readFromURL(file)
      : readFromDisk(file)
    : null;

// musicgen handler
export async function musicgenHandler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  const body = JSON.parse(req.body);
  const result = await musicgen(body);
  res.status(200).json({ data: result });
}

async function musicgen({ melody, ...params }) {
  const melodyBlob = await getFile(melody);

  const app = await client("http://127.0.0.1:7865/");
  const result = await app.predict("/musicgen", [
    // {
    //   text: "bass",
    //   melody: null,
    //   model: "small",
    //   duration: 1,
    //   topk: 250,
    //   topp: 0,
    //   temperature: 1.0,
    //   cfg_coef: 3.0,
    //   seed: -1,
    //   use_multi_band_diffusion: false,
    // },
    {
      melody: null,
      ...params,
    },
    melodyBlob, // blob in 'Melody (optional)' Audio component
  ]);
  return result?.data;
}