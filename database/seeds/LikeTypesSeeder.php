<?php

use Illuminate\Database\Seeder;
use App\Models\LikeTypes;

class LikeTypesSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        $types = [
            'like',
            'smile',
            'love',
            'disappointment',
            'laugh'
        ];

        foreach ($types as $type) {
            LikeTypes::create([
                'type' => $type,
                'description' => 'description'
            ]);
        }
    }
}
