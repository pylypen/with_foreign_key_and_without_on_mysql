<?php

use Illuminate\Database\Seeder;
use App\Models\ReportTypes;

class ReportTypesSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        $types = [
            'Type I',
            'Type II',
            'Type III'
        ];

        foreach ($types as $type) {
            ReportTypes::create([
                'type' => $type,
                'description' => 'Description'
            ]);
        }
    }
}
