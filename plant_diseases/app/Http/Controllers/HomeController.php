<?php
// app/Http/Controllers/HomeController.php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\File;
use Illuminate\Support\Str;

class HomeController extends Controller
{
    public function index()
    {
        return view('home.index');
    }

    public function store(Request $request)
    {
        set_time_limit(120);

        $request->validate([
            'image' => 'required|image|max:5120',
        ]);

        $uploadDir = public_path('uploads');
        if (! File::exists($uploadDir)) {
            File::makeDirectory($uploadDir, 0755, true);
        }

        $file     = $request->file('image');
        $filename = time() . '_' . Str::random(8)
            . '.' . $file->getClientOriginalExtension();
        $file->move($uploadDir, $filename);

        $relativePath = 'uploads/' . $filename;
        $absolutePath = $uploadDir . DIRECTORY_SEPARATOR . $filename;

        $exePath = realpath(base_path('analyzer/run_analyzer.bat'));
        $cmd     = escapeshellarg($exePath) . ' ' . escapeshellarg($absolutePath);

        exec($cmd . ' 2>&1', $outputLines, $exitCode);
        $rawOutput = implode("\n", $outputLines);
        $clean     = preg_replace('/\e\[[\d;]*[A-Za-z]/', '', $rawOutput);

        if (preg_match('/([A-Za-z0-9_]+:\d+\.\d+%)(?!.*[:%])/', $clean, $m)) {
            $result = $m[1];
        } else {
            $lines  = array_filter(array_map('trim', explode("\n", $clean)));
            $result = end($lines) ?: 'No result';
        }

        if (strpos($result, ':') !== false) {
            list($label, $percent) = explode(':', $result, 2);
            $label   = str_replace('_', ' ', $label);
            $result  = $label . ':' . $percent;
        }

        if ($request->ajax()) {
            if ($exitCode !== 0) {
                return response()->json([
                    'error'   => 'Analyzer failed',
                    'details' => $clean,
                ], 500);
            }
            return response()->json([
                'imageUrl' => asset($relativePath),
                'analysis' => $result,
            ]);
        }

        return redirect()
            ->route('home.index')
            ->with('imageUrl', asset($relativePath))
            ->with('analysis', $result);
    }
}
