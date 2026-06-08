import { useEffect, useState } from "react";

import UserTable from "../../components/collaboration/user/UserTable";
import UserFormModal from "../../components/collaboration/user/UserFormModal";

import {
  getOrganizationUsers,
  createOrganizationUser,
  updateOrganizationUser,
  activateUser,
  deactivateUser,
} from "../../services/collaboration/organizationUserService";

export default function OrganizationUsers() {
  const [users, setUsers] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [showModal, setShowModal] =
    useState(false);

  const [editingUser, setEditingUser] =
    useState(null);

  const loadUsers = async () => {
    try {
      const data =
        await getOrganizationUsers();

      setUsers(data || []);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, []);

  const handleCreate = () => {
    setEditingUser(null);
    setShowModal(true);
  };

  const handleEdit = (
    user
  ) => {
    setEditingUser(user);
    setShowModal(true);
  };

  const handleSubmit = async (
    payload
  ) => {
    try {
      if (editingUser) {
        await updateOrganizationUser(
          editingUser.id,
          payload
        );
      } else {
        await createOrganizationUser(
          payload
        );
      }

      setShowModal(false);
      setEditingUser(null);

      await loadUsers();
    } catch (error) {
      console.error(error);
      alert(
        error?.response?.data?.detail ||
          "Operation failed"
      );
    }
  };

  const handleActivate =
    async (user) => {
      try {
        await activateUser(
          user.id
        );

        await loadUsers();
      } catch (error) {
        console.error(error);
      }
    };

  const handleDeactivate =
    async (user) => {
      try {
        await deactivateUser(
          user.id
        );

        await loadUsers();
      } catch (error) {
        console.error(error);
      }
    };

  if (loading) {
    return (
      <div>
        Loading users...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">
            Organization Users
          </h1>

          <p className="text-gray-500">
            Manage users inside your
            organization
          </p>
        </div>

        <button
          onClick={handleCreate}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          Create User
        </button>
      </div>

      {/* Table */}
      <UserTable
        users={users}
        onEdit={handleEdit}
        onActivate={
          handleActivate
        }
        onDeactivate={
          handleDeactivate
        }
      />

      {/* Modal */}
      {showModal && (
        <UserFormModal
          editingUser={
            editingUser
          }
          onClose={() => {
            setShowModal(
              false
            );

            setEditingUser(
              null
            );
          }}
          onSubmit={
            handleSubmit
          }
        />
      )}
    </div>
  );
}