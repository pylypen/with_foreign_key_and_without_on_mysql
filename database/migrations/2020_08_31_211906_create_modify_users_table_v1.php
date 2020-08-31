<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateModifyUsersTableV1 extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::table('modify_users_table_v1', function (Blueprint $table) {
            $table->unsignedBigInteger('avatar_id')->nullable();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::table('modify_users_table_v1', function (Blueprint $table) {
            $table->removeColumn('avatar_id');
        });
    }
}
