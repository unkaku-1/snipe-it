<?php

return [
    'activated_help_text' => 'This user can login',
    'activated_disabled_help_text' => 'You cannot edit activation status for your own account.',
    'assets_user'       => 'Assets assigned to :name',
    'bulk_update_warn'	=> 'You are about to edit the properties of :user_count users. Please note that you cannot change your own user attributes using this form, and must make edits to your own user individually.',
    'bulk_update_help'	=> 'This form allows you to update multiple users at once. Only fill in the fields you need to change. Any fields left blank will remain unchanged.',
    'current_assets'    => 'Assets currently checked out to this user',
    'clone'             => 'Clone User',
    'contact_user'      => 'Contact :name',
    'edit'              => 'Edit User',
    'filetype_info'     => 'Allowed filetypes are png, gif, jpg, jpeg, doc, docx, pdf, txt, zip, and rar.',
    'history_user'      => 'History for :name',
    'info'				=> 'Info',
    'restore_user'		=> 'Click here to restore them.',
    'last_login'        => 'Last Login',
    'ldap_config_text'  => 'LDAP configuration settings can be found Admin > Settings. The (optional) selected location will be set for all imported users.',
    'print_assigned'    => 'Print All Assigned',
    'email_assigned'    => 'Email List of All Assigned',
    'user_notified'     => 'User has been emailed a list of their currently assigned items.',
    'users_notified'    => 'The user has been emailed a list of their currently assigned items.|:count users have been emailed a list of their currently assigned items.',
    'users_notified_warning' => ':count user has been emailed a list of their currently assigned items, however :no_email users did not have an email address so could not be emailed.|:count users have been emailed a list of their currently assigned items, however :no_email user(s) did not have an email address so could not be emailed.',
    'auto_assign_label' => 'Include this user when auto-assigning eligible licenses',
    'auto_assign_help'  => 'Skip this user in auto assignment of licenses',
    'software_user'     => 'Software Checked out to :name',
    'send_email_help'   => 'You must provide an email address for this user to send them credentials. Emailing credentials can only be done on user creation. Passwords are stored in a one-way hash and cannot be retrieved once saved.',
    'view_user'         => 'View User :name',
    'usercsv'           => 'CSV file',
    'two_factor_admin_optin_help' => 'Your current admin settings allow selective enforcement of two-factor authentication.  ',
    'two_factor_enrolled' => '2FA Device Enrolled ',
    'two_factor_active'   => '2FA Active ',
    'user_deactivated'  => 'User cannot login',
    'user_activated'  => 'User can login',
    'activation_status_warning' => 'Do not change activation status',
    'group_memberships_helpblock' => 'Only superadmins may edit group memberships.',
    'superadmin_permission_warning' => 'Only superadmins may grant a user superadmin access.',
    'admin_permission_warning' => 'Only users with admins rights or greater may grant a user admin access.',
    'remove_group_memberships' => 'Remove Group Memberships',
    'warning_deletion_information' => 'You are about to checkin ALL items from the :count user(s) listed below. Super admin names are highlighted in red.',
    'update_user_assets_status' => 'Update all assets for these users to this status',
    'checkin_user_properties' => 'Check in all properties associated with these users',
    'remote_label'   => 'This is a remote user',
    'remote'   => 'Remote',
    'remote_help' => 'This can be useful if you need to filter by remote users who never or rarely come into your physical locations.',
    'not_remote_label' => 'This is not a remote user',
    'vip_label' => 'VIP user',
    'vip_help' => 'This can be helpful to mark important people in your org if you would like to handle them in special ways.',
    'create_user' => 'Create a user',
    'create_user_page_explanation' => 'This is the account information you will use to access the site for the first time.',
    'email_credentials' => 'Email credentials',
    'email_credentials_text' => 'Email my credentials to the email address above',
    'next_save_user' => 'Next: Save User',
    'all_assigned_list_generation' => 'Generated on:',
    'email_user_creds_on_create' => 'Email this user their credentials?',
    'department_manager' => 'Department Manager',
];
