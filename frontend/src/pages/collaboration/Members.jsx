import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  useParams,
} from "react-router-dom";

import MemberTable from "../../components/collaboration/member/MemberTable";

import MemberFormModal from "../../components/collaboration/member/MemberFormModal";

import {
  getMembers,
  addMember,
  removeMember,
  updateMemberRole,
} from "../../services/collaboration/memberService";

export default function Members() {
  const { workspaceId } =
    useParams();

  const [members, setMembers] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [showModal, setShowModal] =
    useState(false);

  const [search, setSearch] =
    useState("");

  const loadMembers =
    useCallback(async () => {
      try {
        setLoading(true);

        const data =
          await getMembers(
            workspaceId,
            search
          );

        setMembers(data);
      } catch (error) {
        console.error(error);

        setMembers([]);
      } finally {
        setLoading(false);
      }
    }, [
      workspaceId,
      search,
    ]);

  useEffect(() => {
    loadMembers();
  }, [loadMembers]);

  const handleAdd =
    async (payload) => {
      try {
        await addMember({
          workspace_id:
            Number(
              workspaceId
            ),
          ...payload,
        });

        setShowModal(false);

        await loadMembers();
      } catch (error) {
        console.error(error);
      }
    };

  const handleRemove =
    async (member) => {
      const confirmed =
        window.confirm(
          "Remove member from workspace?"
        );

      if (!confirmed) {
        return;
      }

      try {
        await removeMember(
          workspaceId,
          member.user_id
        );

        await loadMembers();
      } catch (error) {
        console.error(error);
      }
    };

  const handleRoleChange =
    async (
      member,
      role
    ) => {
      try {
        await updateMemberRole({
          workspace_id:
            Number(
              workspaceId
            ),
          user_id:
            member.user_id,
          role,
        });

        await loadMembers();
      } catch (error) {
        console.error(error);
      }
    };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">
          Workspace Members
        </h1>

        <button
          onClick={() =>
            setShowModal(true)
          }
          className="
            bg-blue-600
            text-white
            px-4 py-2
            rounded-lg
          "
        >
          Add Member
        </button>
      </div>

      <div>
        <input
          type="text"
          placeholder="Search members..."
          value={search}
          onChange={(e) =>
            setSearch(
              e.target.value
            )
          }
          className="
            w-full
            md:w-80
            border
            rounded-lg
            px-3
            py-2
          "
        />
      </div>

      {loading ? (
        <div>
          Loading members...
        </div>
      ) : members.length === 0 ? (
        <div className="text-gray-500">
          No members found
        </div>
      ) : (
        <MemberTable
          members={members}
          onRemove={
            handleRemove
          }
          onRoleChange={
            handleRoleChange
          }
        />
      )}

      {showModal && (
        <MemberFormModal
          onClose={() =>
            setShowModal(false)
          }
          onSubmit={
            handleAdd
          }
        />
      )}
    </div>
  );
}